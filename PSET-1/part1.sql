/* Danny Hong ECE-464 Databases Problem Set 1 Part 1 */

/* Question 1: List, for every boat, the number of times it has been reserved, excluding those boats that have never been reserved (list the id and the name).*/
select Boats.bid, Boats.bname, count(*) as Number_of_Reservations from Boats, Reserves
where Boats.bid = Reserves.bid group by Boats.bid having Number_of_Reservations > 0;

/* Question 2: List those sailors who have reserved every red boat (list the id and the name).*/
select Sailors.sid, Sailors.sname from Sailors, Boats
where not exists(
    select Boats.bid from Boats 
    where not exists(
        select Reserves.bid from Reserves where Reserves.bid = Boats.bid and Boats.color = 'red'));

/* Question 3: List those sailors who have reserved only red boats. */
select distinct Sailors.sid, Sailors.sname from Sailors, Reserves, Boats
where Boats.color = 'red' and Sailors.sid = Reserves.sid and Reserves.bid = Boats.bid
and Sailors.sid not in(
    select Sailors.sid from Sailors, Reserves, Boats
    where Boats.color != 'red' and Sailors.sid = Reserves.sid and Boats.bid = Reserves.bid);

/* Question 4: For which boat are there the most reservations? */
select Boats.bid, Boats.bname, count(*) as Number_of_Reservations from Boats, Reserves
where Boats.bid = Reserves.bid group by Boats.bid order by Number_of_Reservations desc limit 1;

/* Question 5: Select all sailors who have never reserved a red boat. */
select Sailors.sid, Sailors.sname from Sailors 
where Sailors.sid not in(
    select Reserves.sid from Reserves inner join Boats on Boats.bid = Reserves.bid where Boats.color = 'red')
order by Sailors.sid;

/* Question 6: Find the average age of sailors with a rating of 10. */
select avg(Sailors.age) as Average_Sailors_Age from Sailors
where Sailors.rating = 10;

/* Question 7: For each rating, find the name and id of the youngest sailor. */
select Sailors.sid, Sailors.sname, Sailors.rating, Sailors.age from Sailors
having Sailors.age <= all(
    select Sailors_1.age from Sailors Sailors_1 where Sailors.rating = Sailors_1.rating)
order by Sailors.rating;

/* Question 8: Select, for each boat, the sailor who made the highest number of reservations for that boat. */
select X.bid, X.bname, X.sid, X.sname, max(Number_of_Reservations) as Number_of_Reservations from(
    select Sailors.sname, Boats.bname, Reserves.sid, Reserves.bid, count(*) as Number_of_Reservations from Sailors, Boats, Reserves
    where Sailors.sid = Reserves.sid and Boats.bid = Reserves.bid group by Reserves.sid, Reserves.bid order by Number_of_Reservations) as X
group by X.sid, X.bid order by X.bid;