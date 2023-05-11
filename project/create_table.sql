DROP TABLE IF EXISTS customer cascade;
DROP TABLE IF EXISTS Product cascade;
DROP TABLE IF EXISTS Brand cascade;
DROP TABLE IF EXISTS Category cascade;
DROP TABLE IF EXISTS Subcategory cascade;
DROP TABLE IF EXISTS BrandHasPdt;
DROP TABLE IF EXISTS CartHasPdt;
DROP TABLE IF EXISTS Bought;
DROP TABLE IF EXISTS SubCatHasBrand;
DROP TABLE IF EXISTS WLhasPdt;
DROP TABLE IF EXISTS CatHasSubcat;
DROP TABLE IF EXISTS Productlink;

CREATE TABLE customer(
    user_id int PRIMARY KEY, 
    type varchar NOT NULL,
    name varchar NOT NULL,
    password varchar NOT NULL,
    phone_no bigint NOT NULL,
    email_id varchar NOT NULL,
    address varchar NOT NULL
);

CREATE TABLE Product(
    product_id bigint PRIMARY KEY,
    colour varchar NOT NULL,
    actual_price decimal NOT NULL,
    current_price decimal NOT NULL,
    discount decimal NOT NULL,
    no_of_likes decimal NOT NULL,
    quantity int NOT NULL
);

CREATE TABLE Brand(
    brand_id int PRIMARY KEY,
    brand varchar NOT NULL
);

CREATE TABLE Category(
    category_id int PRIMARY KEY,
    category varchar NOT NULL
);

CREATE TABLE Subcategory(
    subcat_id int PRIMARY KEY,
    subcategory varchar NOT NULL
);


CREATE TABLE BrandHasPdt(
    brand_id int NOT NULL,
    product_id bigint NOT NULL,
    FOREIGN KEY (brand_id) References Brand(brand_id),
    FOREIGN KEY (product_id) References Product(product_id)
);

CREATE TABLE CartHasPdt(
    user_id int NOT NULL,
    product_id bigint NOT NULL,
    pdt_quantity int NOT NULL,
    FOREIGN KEY (user_id) References customer(user_id),
    FOREIGN KEY (product_id) References Product(product_id)
);

CREATE TABLE Bought(
    user_id int NOT NULL,
    product_id bigint NOT NULL,
    FOREIGN KEY (user_id) References customer(user_id),
    FOREIGN KEY (product_id) References Product(product_id)
);

CREATE TABLE SubCatHasBrand(
    subcat_id int NOT NULL,
    brand_id int NOT NULL,
    FOREIGN KEY (subcat_id) References Subcategory(subcat_id),
    FOREIGN KEY (brand_id) References Brand(brand_id)
);

CREATE TABLE WLhasPdt(
    user_id int NOT NULL,
    product_id int NOT NULL,
    FOREIGN KEY (user_id) References customer(user_id),
    FOREIGN KEY (product_id) References Product(product_id)
);

CREATE TABLE CatHasSubcat(
    category_id int NOT NULL,
    subcat_id int NOT NULL,
    FOREIGN KEY (category_id) References Category(category_id),
    FOREIGN KEY (subcat_id) References Subcategory(subcat_id)
);

CREATE TABLE Productlink(
    product_id bigint PRIMARY KEY,
    image varchar NOT NULL
);
