[![Build Status](https://travis-ci.org/sunqingyao/fellow-go.svg?branch=master)](https://travis-ci.org/sunqingyao/fellow-go)
[![Coverage Status](https://coveralls.io/repos/github/sunqingyao/fellow-go/badge.svg?branch=master)](https://coveralls.io/github/sunqingyao/fellow-go?branch=master)

# Here is the home of Fellow Go! Project

Fellow Go! Project aims to provide a platform, where college students can pick up stuff like takeout, toothpaste and shampoo for each other.


### Workflow

##### Basic

1. Mary places an order on our platform, saying _Buy me a Diao's fried rice (valid before 13:15)_
2. In case nobody react to the order, Mary can place a bounty on it.
3. John, who happens to be at the Diao's, sees and takes Mary's order, and they start discussing the details via IM.
4. John buys a Diao's fried rice, brings it to Mary, and Mary pays John with the amount they've agreed upon.

##### Advanced

1. Mary places an order on our platform, saying _Buy me a Diao's fried rice (valid before 13:15)_
2. If nobody react to the order after a while, the platform would suggest Mary to place a bounty on it.
3. Since John is near the Diao's, he would receive a push notification from our platform.
4. John, being interested, takes Mary's order, and they start discussing the details via IM. The platform would then provide relevant information like items' average transaction prices, when possible.
5. Mary stores money to the platform with the amount they've agreed upon. She can also use her balance, if she has any.
6. John buys a Diao's fried rice, and brings it to Mary.
7. The system gives the money to John (i.e. paying him directly or adding the amount to his balance, depending on John's preference), after Mary confirms she has received the good.


### Features to implement:

+ Order <s>placing</s> & taking
  + Tag system
  + Reputation system
+ User registration and <s>log in</s>
  + User authenticating by verify emails
  + Integration with school's CAS authentication system
+ Online payment
  + Alipay support
  + WeChat Pay support
  + Tenpay support
+ User pairing based on geolocation
+ Instant messaging between users
+ Integrated AI
+ RESTful/GraphQL API


### Caveats

+ Since Heroku doesn't grant me write permission to the file system, I cannot create the index file needed by Whoosh. As a result, I changed the search engine backend to `SimpleEngine` to enable basic searching functionality. Please note that _doing so disables advanced searching functionalities such as result filtering._

To use Whoosh backend on your local machine, find the following variable in `settings.py`

    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
        },
    }
    
change it to

    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
            'PATH': os.path.join(os.path.dirname(__file__), 'whoosh_index'),
        },
    }
    
and run `python manage.py update_index`.


### Contact

You can reach me at sunqingyao19970825 at gmail.com, or 10152160153 at ecnu.cn
