for any deploy you must use this commands:
</br>
python manage.py makemigrations
</br>
python manage.py migrate
</br>
python manage.py runserver
</br>
</br>
but if this is your first time you have to use:
</br>
python manage.py initialsetup
</br>
python manage.py createsuperuser
</br>
before runserver
</br>
</br>
</br>
Context :
</br>
</br>
MVP Version:
</br>
- Homepage creation ✅  </br>
- User wallet ✅  </br>
- Site treasury ✅  </br>
- User registration ✅  </br>
- User login ✅  </br>
- User logout ✅  </br>
- Purchase 1 product (will be moved to shopping cart in future versions) ✅  </br>
- Wallet recharge (no payment gateway) ❌  </br>
</br>
---
</br>
Version 1:
</br>
- Product creation ✅  </br>
- Verification code for account creation ✅  </br>
- User roles added ✅  </br>
- Role-based permissions configured and implemented ✅  </br>
- Auction system added ✅  </br>
- Auction products defined ✅  </br>
- Auction bids ✅  </br>
- Debt management for auctions (second bidder cannot register) ✅  </br>
- Product categorization ✅  </br>
</br>
---
</br>
Version 2:
</br>
- Shopping cart added ✅  </br>
- Address and postal code collection on checkout page ✅  </br>
- Wishlist added (no transfer to purchase page yet) ✅  </br>
- Updated requirements ✅  </br>
- Updated .gitignore ✅  </br>
- Admin panel UI added in deployment ✅  </br>
- Artist profiles added ✅  </br>
- Artist profile editing ✅  </br>
</br>
---
</br>
Latest Updates:
</br>
- Rewritten responses in JSON format ✅  </br>
- Atomic transactions for critical operations and changes ✅  </br>
- Optimized and prevented N+1 query issues ✅</br>
