# JWT authentication using AWS Cognito and Google as IdP

In this article we will go over process of authenticating a web app using AWS Cognito & Google as a IdP. Once the user is authenticated the access token will be saved as a cookie which then can be used to access any authenticated end point as long as it’s active.

The first step will be to set up the AWS Cognito user pools & Google. There is great tutorial that goes over all the steps that can be found on the following link:

[AWS Video](https://youtu.be/PkP2GB713rY)

### Web App Workflow
-  Client will be presented with the Google sign in page.
-  Once authenticated the user will be redirected to authenticated URL/endpoint

### Installation
- Rename __example.env__ file to __.env__ file.
- Configure all the variables as per the description below.


| Env Variables      | Explanation                                                                                              |
|--------------------|----------------------------------------------------------------------------------------------------------|
| REDIRECT_URI       | This URL can be located under AWS Cognito > User Pools > [MyPool] > App Client Settings > Callback URLS. |
| CLIENT_ID          | This ID can be found under AWS Cognito > User Pools > [MyPool] > App Client Settings > ID                |
| LOGIN_URL          | https://<myurl>/login?                                                                                   |
| TOKEN_URL          | https://<myurl>/oauth2/token?                                                                            |
| USER_INFO_ENDPOINT | https://<myurl>/oauth2/userInfo                                                                          |
| CLIENT_AUTH        | CLIENT_ID:CLIENT_SECRET                                                                                  |
| PUBLIC_KEY_URL     | https://cognito-idp.{region}.amazonaws.com/{userPoolId}/.well-known/jwks.json                            |
| REGION             | AWS Region. For example: us-west-1                                                                       |
| POOL_ID            | Pool ID is located under: AWS Cognito > User Pools > [MyPool] > General Settings > Pool ID               |


```python
pip3 install -r requirements.txt
flask run
```
