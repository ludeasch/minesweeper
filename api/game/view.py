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
       

    def update(self, request, *args, **kwargs):
     

    def destroy(self, request, *args, **kwargs):
    