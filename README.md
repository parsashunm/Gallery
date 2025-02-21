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
- Homepage creation ✅  
- User wallet ✅  
- Site treasury ✅  
- User registration ✅  
- User login ✅  
- User logout ✅  
- Purchase 1 product (will be moved to shopping cart in future versions) ✅  
- Wallet recharge (no payment gateway) ❌  
</br>
---
</br>
Version 1:
</br>
- Product creation ✅  
- Verification code for account creation ✅  
- User roles added ✅  
- Role-based permissions configured and implemented ✅  
- Auction system added ✅  
- Auction products defined ✅  
- Auction bids ✅  
- Debt management for auctions (second bidder cannot register) ✅  
- Product categorization ✅  
</br>
---
</br>
Version 2:
</br>
- Shopping cart added ✅  
- Address and postal code collection on checkout page ✅  
- Wishlist added (no transfer to purchase page yet) ✅  
- Updated requirements ✅  
- Updated .gitignore ✅  
- Admin panel UI added in deployment ✅  
- Artist profiles added ✅  
- Artist profile editing ✅  
</br>
---
</br>
Latest Updates:
</br>
- Rewritten responses in JSON format ✅  
- Atomic transactions for critical operations and changes ✅  
- Optimized and prevented N+1 query issues ✅
