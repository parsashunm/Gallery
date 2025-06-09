 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/README.md b/README.md
index 330757814c5d9f1ca67b6652c04a36c6eebd5bf3..8ee36f4f3130ad5558837ba9c5b56143dbf768df 100644
--- a/README.md
+++ b/README.md
@@ -1,67 +1,48 @@
-for any deploy you must use this commands:
-</br>
-python manage.py makemigrations
-</br>
-python manage.py migrate
-</br>
-python manage.py runserver
-</br>
-</br>
-but if this is your first time you have to use:
-</br>
-python manage.py initialsetup
-</br>
-python manage.py createsuperuser
-</br>
-before runserver
-</br>
-</br>
-</br>
-Context :
-</br>
-</br>
-MVP Version:
-</br>
-- Homepage creation ✅  </br>
-- User wallet ✅  </br>
-- Site treasury ✅  </br>
-- User registration ✅  </br>
-- User login ✅  </br>
-- User logout ✅  </br>
-- Purchase 1 product (will be moved to shopping cart in future versions) ✅  </br>
-- Wallet recharge (no payment gateway) ❌  </br>
-</br>
+# NFT Gallery
+
+This project is a digital art marketplace built with **Django 5.1** and the **Django REST Framework**. Users can register, manage a wallet, and buy or auction artworks. The application uses WebSockets via Django Channels and background tasks via Celery.
+
+## Features
+- User registration and login with OTP confirmation
+- Role based permissions (buyer, artist, presenter, admin)
+- Wallet management and a central treasury
+- Product creation with categories and attributes
+- Auction system with live updates
+- Shopping cart and wishlist
+- Artist profiles and editing
+- JSON API responses with atomic transactions
+
+## Getting Started
+1. Install Python 3.10 and clone this repository.
+2. Install dependencies using [Pipenv](https://pipenv.pypa.io/en/latest/):
+   ```bash
+   pipenv install
+   ```
+3. Run the initial database migrations:
+   ```bash
+   python manage.py makemigrations
+   python manage.py migrate
+   ```
+4. On the first run, create initial data and an administrator:
+   ```bash
+   python manage.py initialsetup
+   python manage.py createsuperuser
+   ```
+5. Start the development server:
+   ```bash
+   python manage.py runserver
+   ```
+
+## Development
+- The project uses Celery for asynchronous tasks. Update `celery_conf.py` if you need to modify the broker settings.
+- WebSocket routes are defined in `products/routing.py` and configured in `NFTgallery/asgi.py`.
+- Environment-specific settings can be adjusted in `NFTgallery/settings.py`.
+
+## Version History
+- **MVP** – basic homepage, wallet, site treasury, authentication flows, single-product purchase
+- **Version 1** – product creation, account verification codes, user roles and permissions, auctions, debt management, categories
+- **Version 2** – shopping cart, checkout addresses, wishlist, improved admin UI, artist profiles
+- **Latest updates** – JSON responses, atomic operations and N+1 query prevention
+
 ---
-</br>
-Version 1:
-</br>
-- Product creation ✅  </br>
-- Verification code for account creation ✅  </br>
-- User roles added ✅  </br>
-- Role-based permissions configured and implemented ✅  </br>
-- Auction system added ✅  </br>
-- Auction products defined ✅  </br>
-- Auction bids ✅  </br>
-- Debt management for auctions (second bidder cannot register) ✅  </br>
-- Product categorization ✅  </br>
-</br>
----
-</br>
-Version 2:
-</br>
-- Shopping cart added ✅  </br>
-- Address and postal code collection on checkout page ✅  </br>
-- Wishlist added (no transfer to purchase page yet) ✅  </br>
-- Updated requirements ✅  </br>
-- Updated .gitignore ✅  </br>
-- Admin panel UI added in deployment ✅  </br>
-- Artist profiles added ✅  </br>
-- Artist profile editing ✅  </br>
-</br>
----
-</br>
-Latest Updates:
-</br>
-- Rewritten responses in JSON format ✅  </br>
-- Atomic transactions for critical operations and changes ✅  </br>
-- Optimized and prevented N+1 query issues ✅</br>
+Built with ❤ using Django.
 
EOF
)