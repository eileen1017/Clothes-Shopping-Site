### FunShop Creative Project ###   

#### Description :   
we had created a shopping website using React.js for our front-end, flask for back-end and MySQL for database.     

#### Instruction for Compilation:   
1. MySQL: Open app.py and Change **app.config['MYSQL_USER'] = 'lilin1'** and **app.config['MYSQL_PASSWORD'] = 'lilin1017'** these two fields with your local database. and GO to main folder and find the file shopping.sql, RUN **mysql -u YOURUSERNAME -p**, then RUN **source shopping.sql**.   
2. Open another terminal or exit MySQL, RUN **python app.py**.   
3. Finally open another terminal, go to client folder and RUN **npm start**, the webpage will automatically open our shopping site for you.   
4. Then it's time to enjoy surfing our website.   


#### Basic Functionalities:   
1. Users can register and log in.   

**Without login   
2. User can access to home page, login page and register page.   

**With login   
3. Users can browse throughout our products by category Men and Women's apparels with prices.   
4. Users can view their carts to edit quantity of products and it will display with a total price and price with St. Louis sale tax and total price after tax.   
5. Users can add products to their carts and delete products from their carts.   
6. Users can edit product quantity in their carts.   
7. Users can add products to their wishlist for interested products and delete products from their wishlist.
8. Users can click on items's picture and view detail information about the items.   
9. In detail page, they can view comments and add comments if the user has purchased this item before and users cannot add comment repeatly.   
10. Users can set the price to filter the products   
11. Users can add and delete friends, but they cannot modify others wishlist and shopping cart.   
12. Users can have a list of product they bought in the past, and the list cannot be modified.   

#### Creative Portion:   
1. Users can view their friends purchased products without duplicated orders. If they like it, they can add to their cart or wishlists. They can view detail by clicking on pictures of the products.   
2. In our home page, we created a weather diplay window to tell user what weather it is in St. Louis.   
3. Base on weather, we will recommend suitable clothes to our users.   
4. User can search a product by categories. If they type jackets, all the jacket in men's or women's page will diplayed.   
5. Users are able to change their password. After successfully changing the password, they will be directed to login page and asked for relog in.   


#### Some useful installation for running Flask   
pip install Flask.  
sudo pip install flask_bcrypt   
sudo pip install flask_cors   
sudo pip install flask_jwt_extended   
sudo pip install flask_mysqldb   

