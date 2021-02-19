# Accounts API
This is the documentation related to how to use the user APIs. I used the dj-rest-auth library promoted by django rest framework to handle the user app

## Registration
Endpoint to create a new user account 

*/api/v1/accounts/registration/*

**Method:** POST

**Parameters:**

Name | description 
------ | ------ |
`email` | string  |
`username` |string |
`password1`	|string	|
`password2`	|string	|

*Note: password2 is the confirmation of password1*

**Returns:** access token string

**Example:**
``python
	{
		'key': '1fh43hf83h87h43f3hfh438fh438fh8yfh438fh'
	}
```


## Login
Endpoint to login into the application 

*/api/v1/accounts/login/*

**Method:** POST

**Parameters:**

Name | description 
------ | ------ |
`email` | string  |
`password`	|string	|

**Returns:** access token string

**Example:**
``python
	{
		'key': '1fh43hf83h87h43f3hfh438fh438fh8yfh438fh'
	}
```


## User
Endpoint to return/change the user data.

**User token authentication required**

*/api/v1/accounts/user/*
**Method:** GET

**Returns:** json user response 

**Example:**
``python
	{
    "pk": 1,
    "email": "test@ddd.com",
    "first_name": "juan",
    "last_name": "carlos"
}
```


**Method:** PUT

**Parameters:**

Name | description 
------ | ------ |
`first_name` | string  |
`last_name`	|string	|

**Returns:** json user response 

**Example:**
``python
	{
    "pk": 1,
    "email": "test@ddd.com",
    "first_name": "juan",
    "last_name": "carlos"
}
```


## Change password
Endpoint to login into the application 

**User token authentication required**

*/api/v1/accounts/password/change/*

**Method:** POST

**Parameters:**

Name | description 
------ | ------ |
`new_password1` | string  |
`new_password2`	|string	|

**Returns:** json message

**Example:**
``python
	{
    	"detail": "New password has been saved."
	}
```
