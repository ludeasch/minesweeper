class MineseeperViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    CustomCampaignGenericViewSet,
):
    queryset = Game.objects.none()
    serializer_class = GameSerializer
    ordering_fields = ["date_modified"]
    permission_classes = (IsAuthenticated,)
    filterset_fields = ("id",)

    def get_serializer_context(self):
        return {"user": self.request.user, "request": self.request}

    def get_queryset(self):
        return Game.objects.filter(user_id=self.request.user_id)

    def create(self, request, *args, **kwargs):
        response = super(CampaignViewSet, self).create(request, *args, **kwargs)
        campaign = Campaign.objects.get(id=response.data.get("id"), brand=request.user)

        self._save_payment_ranges(request, response, campaign)
        self._save_shopify_models(request, response, campaign)

        return response

    def update(self, request, *args, **kwargs):
        campaign = self.get_object()

        # If the 'Content Submitted By' date was updated
        # because the campaign was extended
        # 1. We mark the 'Overdue Content' notifications as unread
        # 1. to notificate the users again
        # 2. Restart the 'times_content_due_email_sent' counter to 0
        # 2. in case they got the limit (5)
        if request.data["date_sent"] != campaign.date_sent:
            Notification.objects.filter(
                campaingmatch__campaign=campaign,
                seen=True,
                type=Notification.TYPE_OVERDUE_CONTENT,
            ).update(seen=False)
            CampaingMatch.objects.filter(campaign=campaign).update(
                times_content_due_email_sent=0
            )

        response = super(CampaignViewSet, self).update(request, *args, **kwargs)
        campaign = Campaign.objects.get(id=kwargs.get("pk"), brand=request.user)

        # delete all and add the updated ones as new
        campaign.payment_ranges.all().delete()
        self._save_payment_ranges(request, response, campaign)
        self._save_shopify_models(request, response, campaign)

        return response

    def destroy(self, request, *args, **kwargs):
        """
        Only drafts campaigns can be deleted
        """

        campaign = self.get_object()
        if not campaign.draft_mode:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"Error": "This campaign cannot be deleted, this is not a draft"},
            )
        response = super(CampaignViewSet, self).destroy(request, *args, **kwargs)
        return response

    @action(detail=False, methods=("get",))
    def brand_campaing_list_all(self, request, *args, **kwargs):
        """
        Get all campaigns for a Brand
        Only need the name of the campaign
        """
        campaigns = (
            Campaign.objects.get_by_brand_without_drafts(request.user)
            .only("id", "name")
            .order_by("-date_added")
        )
        serializer = CampaignSmallSerializer(campaigns, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=("get",))
    def shipping_info(self, request, *args, **kwargs):
        campaign = self.get_object()
        if campaign.brand_id != request.user.id:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"Error": "You don't have permission to create the export"},
            )

        # Receives the parameter to know from which tab the file was requested
        url_ends_with = request.GET.get("tab")
        # only matches for the current brand
        tab_status = {
            # If the request comes from campaign/pk/accepted
            "Accepted": [CampaingMatch.STATUS_ACCEPTED],
            # If the request comes from campaign/pk/chat
            "Chat": [CampaingMatch.STATUS_CHAT, CampaingMatch.STATUS_APPLY],
        }
        match_status = tab_status.get(url_ends_with)
        if match_status is None:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"Error": "Export file could not be created"},
            )

        response = HttpResponse(content_type="text/csv")
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        filename = f'{campaign.name.replace(" ", "_")}_{date}_Shipping_info.csv'
        response["Content-Disposition"] = f'attachment; filename="{filename}"'

        CampaignShippingExportController(campaign).export_shipping_info(
            response, match_status
        )

        return response

    @action(detail=True, methods=("get",))
    def approved_assets(self, request, *args, **kwargs):
        """
        Returns the approved photos and videos
        from a brand along with the campaign their belong
        """
        # TODO THIS IS NOT A DETAIL VIEW BECAUSE RETURNS INFORMATION
        # FOR A LOT OF CAMPAIGNS
        photos = (
            CampaignPhoto.objects.filter(
                camp_group__campaign__brand=request.user, once_accepted=True
            )
            .annotate(
                camp_id=F("camp_group__campaign__id"),
                user_name=F("users__name"),
                instagram_username=F("users__instagramaccount__username"),
            )
            .values()
        )
        videos = (
            CampaignVideo.objects.filter(
                camp_group__campaign__brand=request.user, once_accepted=True
            )
            .annotate(
                camp_id=F("camp_group__campaign__id"),
                user_name=F("users__name"),
                instagram_username=F("users__instagramaccount__username"),
            )
            .values()
        )

        return Response(
            status=200, data={"approved_videos": videos, "approved_photos": photos}
        )

    @action(detail=True, methods=("get",))
    def expected_budget(self, request, *args, **kwargs):
        """
        Returns the total expected budget to be paidbased on the campaign compenstation
        type and matches' quantity followers
        """
        campaign = self.get_object()
        return Response(data=campaign.get_expected_budget())

    @action(detail=True, methods=("get",))
    def get_payout_amount(self, request, *args, **kwargs):
        """Retrives the amount to pay and creators to be paid"""
        # TODO should not access the queryset should use get_object
        try:
            camp = get_object_or_404(Campaign, brand=request.user, pk=kwargs.get("pk"))
        except Exception as e:
            logging.exception(e)
            return Response(status=400, data=[])
        matches = CampaingMatch.objects.filter(
            campaign__id=kwargs.get("pk"),
            status=CampaingMatch.STATUS_COMPLETED,
            paymentsmatch_set__isnull=True,
        )
        amount = 0
        cant_creators = matches.count()
        ranges = camp.payment_ranges.all().order_by("max_followers")
        lr_value = ranges.last().max_followers
        for cm in matches:
            amount += calc_payment_payout(cm.followers, ranges, lr_value)
        return Response(status=200, data={"creators": cant_creators, "amount": amount})

    @action(detail=True, methods=("post",))
    def campaign_payout(self, request, *args, **kwargs):
        """
        Makes a payout for a campaigns
        Pays all the creators in completed tab that hasn't been payed yet.
        """
        # TODO this should use get_object
        try:
            camp = get_object_or_404(Campaign, brand=request.user, pk=kwargs.get("pk"))
        except Exception as e:
            logging.exception(e)
            return Response(status=400, data={"error": "Campaign does not exists"})

        matches = CampaingMatch.objects.filter(
            campaign=camp,
            status=CampaingMatch.STATUS_COMPLETED,
            paymentsmatch_set__isnull=True,
        )
        without_paypal = matches.filter(user__paypal_account__isnull=True)
        matches = matches.filter(user__paypal_account__isnull=False)
        need_pp = None

        if without_paypal.count() > 0:

            # create message for matches that doesn't have paypal email set it up
            without_msg = []
            for wp in without_paypal:
                without_msg.append(
                    create_message(
                        wp,
                        request.user,
                        CampaingMessages.PAYPAL_PAYMENT_CREATE,
                        True,
                        False,
                    )
                )

            # bulk create messages for accounts that needs to add a paypal email
            need_pp = CampaingMessages.objects.bulk_create(without_msg)
            if matches.count() == 0:
                return Response(
                    status=200,
                    data={
                        "error": "Creators needs to add a paypal email account",
                        "error_data": MessageSerializer(need_pp, many=True).data,
                    },
                )

        payout = Payout()
        items = []
        tot_amount = 0
        has_paid_msg = []

        for cm in matches:
            # calc the amount to pay matches that have paypal email
            ranges = camp.payment_ranges.all().order_by("max_followers")
            lr_value = ranges.last().max_followers
            item_amount = calc_payment_payout(cm.followers, ranges, lr_value)
            items.append((cm.user.paypal_account.email, item_amount))
            tot_amount += item_amount

        braintree_ac = camp.brand.braintree_account
        fees = 0
        fid = 0

        if tot_amount > braintree_ac.funds:
            return Response(
                status=status.HTTP_402_PAYMENT_REQUIRED,
                data={"status": 402, "error": "Insuficient funds"},
            )

        try:
            res = payout.create_payout(items)
            if res.status_code == 201:
                # Reduce funds
                braintree_ac.funds -= tot_amount
                braintree_ac.save()
                tfees = (
                    braintree_ac.transaction_set.last()
                )  # lets assume that always pays with the last charged money
                fees = tfees.fees
                fid = tfees.id

                transactions = []
                r = json.loads(res.content)
                payout_id = r.get("payout_batch_id")

                if payout_id:
                    payout_id = payout_id.get("batch_header")

                for i in range(0, matches.count()):
                    cm = matches[i]
                    item = items[i]
                    has_paid_msg.append(
                        create_message(cm, request.user, "has paid", False, False)
                    )
                    transactions.append(
                        Transaction(
                            campaing_match=cm,
                            amount=item[1],
                            charge_id=payout_id,
                            type_transaction=Transaction.TYPE_PAYPAL,
                            fees=fees,
                            intent="pay-with-charge-{}".format(str(fid)),
                        )
                    )  # to track the payment charge used in a simple way
                    send_email_payday.delay(cm.user.id, camp.id, context="async")

                # bulk create messages for accounts that has been paid
                Transaction.objects.bulk_create(transactions)
                has_paid = CampaingMessages.objects.bulk_create(has_paid_msg)
            else:
                subject = "PayPal Payout error!!!"
                message = res.content.decode("utf-8")
                # sends email with the error
                mail_admins(
                    subject,
                    message,
                    fail_silently=False,
                    connection=None,
                    html_message=None,
                )
                return Response(status=400, data={"error": "Something went wrong"})
        except Exception as e:
            logging.exception(e)
            return Response(status=400, data={"error": "Something went wrong"})

        if need_pp:
            need_pp = MessageSerializer(need_pp, many=True).data

        return Response(
            status=201,
            data={
                "sucess": payout_id,
                "data": MessageSerializer(has_paid, many=True).data,
                "error_data": need_pp,
                "new_funds": braintree_ac.funds,
            },
        )

    @action(detail=True, methods=("post",))
    def auto_approve_content(self, request, *args, **kwargs):
        # Since we aren't managing permissions in CampaignViewSet.permission_classes
        # we check at manager level that user can update the campaign.
        # This is reason the query is filtered by brand.
        campaign = get_object_or_404(Campaign, brand=request.user, pk=kwargs.get("pk"))
        campaign.auto_approve_content = not campaign.auto_approve_content
        campaign.save(update_fields=["auto_approve_content"])
        return Response(
            status=status.HTTP_200_OK,
            data={"auto_approve_content": campaign.auto_approve_content},
        )

    @action(detail=True, methods=("post",))
    def associate_products(self, request, *args, **kwargs):
        """
        Associate the created generic products to a campaign
        """
        campaign = self.get_object()
        products_id = request.data["products_id"]
        amount_of_products_per_creator = request.data.get(
            "amount_of_products_per_creator", None
        )

        if not isinstance(products_id, list):
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"Error": "products_id must be a list of Products ids"},
            )

        try:
            amount_of_products_per_creator = int(amount_of_products_per_creator)
        except Exception:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"Error": "amount of products per creator must be a number"},
            )

        products = Product.objects.get_by_user(self.request.user).get_by_ids(
            products_id
        )
        if not products:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"Error": "You need to select products to associate"},
            )

        # check if there are amount per creator
        # and is less than the products that they selected
        if amount_of_products_per_creator > products.count():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"Error": "There are not enough products to pick"},
            )

        try:
            CampaignProductsController().set_generic_products_to_campagin(
                campaign, products, amount_of_products_per_creator
            )
        except ProductsInMatchError:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    "Error": "Some of the products that will be removed from the campaign are being used by a creator"  # noqa
                },
            )

        return Response(status=status.HTTP_200_OK)
