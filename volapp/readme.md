All endpoints start with localhost:8000/api/v1/

Endpoints
    -SignUp (METHOD GET)
        -endpoint: signup/
        -headers = {
            'Authorization': Bearer {google token}
        }
        -response
            -headers = {
                'Access-Token': Tokens used to implement jwt
                'Refresh-Token': jwt refresh
            }
            -status
                -200: User returned {
                    'id',
                    'email',
                    'streak',
                    'lastPostTime',
                    'joinedOn'
                }
                -201: New User created and returned in same format as above
                -401: Bad Token

    -Get User (METHOD GET)
        -endpoint: user/
        -headers = {
            'Access-Token': Token recieved during signup
            'Refresh-Token': Token recieved during login
        }
        -response
            -headers = {
                'Access-Token': Tokens used to implement jwt
                'Refresh-Token': jwt refresh
            }
            -status
                -200: User returned {
                    'id',
                    'email',
                    'streak',
                    'lastPostTime',
                    'joinedOn'
                }
                -401: Bad Token
                -404: No such User

    -Delete User (METHOD DELETE)
        -endpoint: user/<int:id>
        -headers = {
            'Access-Token': Token recieved during signup
            'Refresh-Token': Token recieved during login
        }
        -response
            -status
                -204: Deleted
                -401: Bad Token
                -404: No such user

    -Upload Post (METHOD POST)
        -endpoint: post/
        -headers = {
            'Access-Token': Token recieved during signup
            'Refresh-Token': Token recieved during login
        }
        -data = {
            'url': Media URL,
            'description': Caption,
            'emotions': Tagged emotions,
            'answers': Answers to questions,
        }
        -response
            -headers = {
                'Access-Token': Tokens used to implement jwt
                'Refresh-Token': jwt refresh
            }
            -status
                -204: Created
                -401: Bad Token
                -404: No Such User


    -Edit Caption (METHOD PATCH)
        -endpoint: post/<int:id>
        -headers = {
            'Access-Token': Token recieved during signup
            'Refresh-Token': Token recieved during login
        }
        -data = {
            'caption': New Caption
        }
        -response
            -headers = {
                'Access-Token': Tokens used to implement jwt
                'Refresh-Token': jwt refresh
            }
            -status
                -204: Edited
                -401: Bad Token/Auth Error
                -404: No Such Post

    -Delete Post (METHOD DELETE)
        -endpoint: post/delete/<int:id>
        -headers = {
            'Access-Token': Token recieved during signup
            'Refresh-Token': Token recieved during login
        }
        -response
            -headers = {
                'Access-Token': Tokens used to implement jwt
                'Refresh-Token': jwt refresh
            }
            -status
                -204: Deleted
                -401: Bad Token/Auth Error
                -404: No Such Post
                -500: Internal Server Error
    
    -Get User Posts (METHOD GET)
        -endpoint: user/post/
        -headers = {
            'Access-Token': Token recieved during signup
            'Refresh-Token': Token recieved during login
        }
        -response
            -headers = {
                'Access-Token': Tokens used to implement jwt
                'Refresh-Token': jwt refresh
            }
            -status
                -200: Array[Posts] | Post Format = {
                    'id',
                    'multimedia',
                    'description',
                    'user',
                    'timestamp',
                    'flagged',
                    'emotions',
                    'answers'
                }
                -401: Bad Token/Auth Error
                -404: No such user

    -Get Latest Feed (METHOD GET)
        -endpoint: feed/latest/
        -headers = {
            'Access-Token': Token recieved during signup
            'Refresh-Token': Token recieved during login
        }
        -response
            -headers = {
                'Access-Token': Tokens used to implement jwt
                'Refresh-Token': jwt refresh
            }
            -status
                -200: Array[Posts] | Post Format = {
                    'id',
                    'multimedia',
                    'description',
                    'user',
                    'timestamp',
                    'flagged',
                    'emotions',
                    'answers'
                }
                -401: Bad Token/Auth Error
    
    -Get Next Set of Posts (METHOD POST)
        -endpoint: feed/next/
        -data = {
            'id': Id of last post visible to user,
            'timestamp': Timestamp of last post visible to user
        }
        -headers = {
            'Access-Token': Token recieved during signup
            'Refresh-Token': Token recieved during login
        }
        -response
            -headers = {
                'Access-Token': Tokens used to implement jwt
                'Refresh-Token': jwt refresh
            }
            -status
                -200: Array[Posts] | Post Format = {
                    'id',
                    'multimedia',
                    'description',
                    'user',
                    'timestamp',
                    'flagged',
                    'emotions',
                    'answers'
                }
                -401: Bad Token/Auth Error