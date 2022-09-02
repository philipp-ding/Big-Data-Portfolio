const dns = require("dns").promises;
const os = require("os");
const express = require("express");
const { addAsync } = require("@awaitjs/express");
const app = addAsync(express());
const mariadb = require("mariadb");
const MemcachePlus = require("memcache-plus");
const inefficient = require("inefficient");

//Connect to the memcached instances
let memcached = null;
let memcachedServers = [];

//Database configuration
const pool = mariadb.createPool({
  host: "my-app-mariadb-service",
  database: "sportsdb",
  user: "root",
  password: "mysecretpw",
  connectionLimit: 5,
});

//Get list of memcached servers from DNS
async function getMemcachedServersFromDns() {
  try {
    let queryResult = await dns.lookup("my-memcached-service", { all: true });
    let servers = queryResult.map((el) => el.address + ":11211");

    //Only create a new object if the server list has changed
    if (memcachedServers.sort().toString() !== servers.sort().toString()) {
      console.log("Updated memcached server list to ", servers);
      memcachedServers = servers;
      //Disconnect an existing client
      if (memcached) await memcached.disconnect();
      memcached = new MemcachePlus(memcachedServers);
    }
  } catch (e) {
    console.log("Error resolving memcached", e);
  }
}

//Initially try to connect to the memcached servers, then each 5s update the list
getMemcachedServersFromDns();
setInterval(() => getMemcachedServersFromDns(), 5000);

//Get data from cache if a cache exists yet
async function getFromCache(key) {
  if (!memcached) {
    console.log(
      `No memcached instance available, memcachedServers = ${memcachedServers}`
    );
    return null;
  }
  return await memcached.get(key);
}

// get Genre data from Database
async function getFromDatabase_genre() {
  let connection;
  let query = "SELECT genre from genres"; // query to select genre from genres

  try {
    connection = await pool.getConnection();
    console.log("Executing query " + query);
    let res = await connection.query(query, []); // execute query
    console.log(res); // show result of query

    if (res) {
      console.log("Query result = ", res);
      return res; // return result of query
    } else {
      return null;
    }
    data;
  } finally {
    if (connection) connection.end();
  }
}

//Get data from database
async function getFromDatabase_popular_genre() {
  let connection;
  let query =
    "SELECT genre,count from popular_genres ORDER BY count DESC LIMIT 10";

  try {
    connection = await pool.getConnection();
    console.log("Executing query " + query);
    let res = await connection.query(query, []); // execute query
    console.log(res); // show result of query

    if (res) {
      console.log("Query result = ", res);
      return res; // return result of query
    } else {
      return null;
    }
    data;
  } finally {
    if (connection) connection.end();
  }
}

// get description of a genre from database
async function getFromDatabase_genre_description(userid) {
  let connection;
  let query = "SELECT * from genres where genre  = ?"; // get a specific genre if meets condition

  try {
    connection = await pool.getConnection();
    console.log("Executing query " + query);
    let res = await connection.query(query, [userid]);
    let row = res[0]; // get the first result of query
    console.log(res);

    if (row) {
      console.log("Query result = ", row);
      return row["description"]; // returns description of genre
    } else {
      return null;
    }
    data;
  } finally {
    if (connection) connection.end();
  }
}

//Send HTML response to client
function send_response(response, top_ten_genres) {
  response.send(`<!DOCTYPE html>
		<html lang="de">
		<head>
			<meta charset="UTF-8">
			<meta name="viewport" content="width=device-width, initial-scale=1.0">
			<title>Musik Genres</title>
			<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/mini.css/3.0.1/mini-default.min.css">
		<style>
			body {background-color: black;}
			h1 {color: white;}
			p {color: white;}
			h2 {color: white;}
			ul {color: white;}
			ol {color: white;}
			a { color: #1DB954;}
			</style>
			</head>
		<body>
			<h1>Musik Genres</h1>
			<p style="margin-bottom:2%"> </p>
			<p>${top_ten_genres} </p>

<hr>
			<h2>Informationen zu der generierten Seite</h4>

			<ul>
				<li>Host ${os.hostname()}</li>
				<li>Date: ${new Date()}</li>
				<li>Memcached Servers: ${memcachedServers}</li>
				<li>Result: <b></b></li>
			</ul>
			</body>
	</html>`);
}

function send_response_genre(response, userid, data) {
  response.send(`<!DOCTYPE html>
		<html lang="de">
		<head>
			<meta charset="UTF-8">
			<meta name="viewport" content="width=device-width, initial-scale=1.0">
			<title>Musik Genres</title>
			<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/mini.css/3.0.1/mini-default.min.css">
			<style>
			body {background-color: black;}
			h1 {color: white;}
			p {color: white;}
			h2 {color: white;}
			ul {color: white;}
			a { color: #1DB954;}

			</style>
		</head>
		<body>
			<h1>${userid}</h1>
			<p>
				${data}
			</p>
			<a href="/" style="color: #1DB954;">Zurück zur Startseite</a>

<hr>
			<h2>Informationen zu der generierten Seite</h2>
			<ul >
				<li>Host ${os.hostname()}</li>
				<li>Date: ${new Date()}</li>
				<li>Memcached Servers: ${memcachedServers}</li>
				<li>Result: <b>${userid}</b></li>
			</ul>
			</body>
	</html>`);
}

// startpage
app.get("/", async function (request, response) {
  Promise.all([getFromDatabase_genre(), getFromDatabase_popular_genre()]).then(
    (values) => {
      const genres = values[0];
      const popular = values[1];

      const genre_html = genres
        .map(
          (m) =>
            `<a href='/genre/${m.genre}' style="color: #1DB954;">${m.genre}</a>`
        )
        .join(", "); // links of genres
      const popularHtml = popular
        .map(
          (pop) =>
            `<li> <a href='/genre/${pop.genre}' style="color: #1DB954;">${pop.genre}</a> (${pop.count} views) </li>`
        )
        .join("\n"); // list elements with Genre titles
      const html = `
			<h2>Top 10 Genres</h2>
			<p>
				<ol style="margin-left: 2em;"> ${popularHtml} </ol>
			</p>
			<h2>Alle Genres</h2>
			<p> ${genre_html} </p>`;

      send_response(response, html);
    }
  );
});

// Page bout a specific genre & a description
app.getAsync("/genre/:id", async function (request, response) {
  let userid = request.params["id"]; // saves parameter of id in userid
  let key = userid;
  let cachedata = await getFromCache(key);

  if (cachedata) {
    console.log(`Cache hit for key=${key}, cachedata = ${cachedata}`);
    send_response_genre(response, userid, cachedata);
  } else {
    console.log(`Cache miss for key=${key}, querying database`);
    let data = await getFromDatabase_genre_description(userid);
    if (data) {
      console.log(`Got data=${data}, storing in cache`);
      if (memcached) await memcached.set(key, data, 30 /* seconds */);
      send_response_genre(response, userid, data);
    } else {
      send_response_genre(response, userid, "No data found");
    }
  }
});

// Add stress test endpoint, cf. https://github.com/bermi/inefficient
app.get("/stress", inefficient);

// Set port to start the app on
app.set("port", process.env.PORT || 8080);

// Start the application
app.listen(app.get("port"), function () {
  console.log("Node app is running at localhost:" + app.get("port"));
});
