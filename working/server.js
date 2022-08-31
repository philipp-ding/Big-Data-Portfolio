const dns = require('dns').promises;
const os = require('os')
const express = require('express')
const { addAsync } = require('@awaitjs/express');
const app = addAsync(express());
const mariadb = require('mariadb')
const MemcachePlus = require('memcache-plus');
const inefficient = require('inefficient');

//Connect to the memcached instances
let memcached = null
let memcachedServers = []

//Database configuration
const pool = mariadb.createPool({
	host: 'my-app-mariadb-service',
	database: 'sportsdb',
	user: 'root',
	password: 'mysecretpw',
	connectionLimit: 5
})

//Get list of memcached servers from DNS
async function getMemcachedServersFromDns() {
	try {
		let queryResult = await dns.lookup('my-memcached-service', { all: true })
		let servers = queryResult.map(el => el.address + ":11211")

		//Only create a new object if the server list has changed
		if (memcachedServers.sort().toString() !== servers.sort().toString()) {
			console.log("Updated memcached server list to ", servers)
			memcachedServers = servers
			//Disconnect an existing client
			if (memcached)
				await memcached.disconnect()
			memcached = new MemcachePlus(memcachedServers);
		}
	} catch (e) {
		console.log("Error resolving memcached", e);
	}
}

//Initially try to connect to the memcached servers, then each 5s update the list
getMemcachedServersFromDns()
setInterval(() => getMemcachedServersFromDns(), 5000)

//Get data from cache if a cache exists yet
async function getFromCache(key) {
	if (!memcached) {
		console.log(`No memcached instance available, memcachedServers = ${memcachedServers}`)
		return null;
	}
	return await memcached.get(key);
}

//Get data from database
async function getFromDatabase(userid) {
	let connection
	let query = 'SELECT * from genres'; // 'SELECT * from genres where genre  = "' + connection.escape(userid)+'" '

	try {
		connection = await pool.getConnection()
		console.log("Executing query " + query)
		let res = await connection.query(query, [userid])
		let row = res[0]
		console.log(res)

		if (row) {
			console.log("Query result = ", row)
			return row["genre"];
		} else {
			return null;
		}
data
	} finally {
		if (connection)
			connection.end()
	}
}


async function getFromDatabase_start() {
	let connection
	let query = 'SELECT genre from genres'; // 'SELECT * from genres where genre  = "' + connection.escape(userid)+'" '

	try {
		connection = await pool.getConnection()
		console.log("Executing query " + query)
		let res = await connection.query(query, [])
		// let row = res[0]
		console.log(res)

		if (res) {
			console.log("Query result = ", res)
			// let result = res["genre"]
			console.log("Query result undefined res = ", res)
			return res//result //row["genre"];
		} else {
			return null;
		}
data
	} finally {
		if (connection)
			connection.end()
	}
}




//Get data from database
async function getFromDatabaseStartpage() {
	let connection
	let query = 'SELECT * from popular_genres ORDER BY count DESC LIMIT 10'; // sorted by & desc !!!

	try {
		connection = await pool.getConnection()
		console.log("Executing query " + query)
		let res = await connection.query(query, [])
		// let row = res[0]
		console.log(res)

		if (res) {
			console.log("Query result = ", res)
			// return row["genre"];
			return res
		} else {
			return null;
		}
data
	} finally {
		if (connection)
			connection.end()
	}
}



//Get data from database
async function getFromDatabaseStartpage_popular() {
	let connection
	let query = 'SELECT genre,count from popular_genres ORDER BY count DESC LIMIT 10'; // sorted by & desc !!!

	try {
		connection = await pool.getConnection()
		console.log("Executing query " + query)
		let res = await connection.query(query, [])
		// let row = res[0]
		console.log(res)

		if (res) {
			console.log("Query result = ", res)
			// return row["genre"];
			return res
		} else {
			return null;
		}
data
	} finally {
		if (connection)
			connection.end()
	}
}







async function getFromDatabase_genre(userid) {
	let connection
	let query = 'SELECT * from genres where genre  = ?' ; // 'SELECT * from genres where genre  = "' + connection.escape(userid)+'" '

	try {
		connection = await pool.getConnection()
		console.log("Executing query " + query)
		let res = await connection.query(query, [userid])
		let row = res[0]
		console.log(res)

		if (row) {
			console.log("Query result = ", row)
			return row["description"];
		} else {
			return null;
		}
data
	} finally {
		if (connection)
			connection.end()
	}
}











//Send HTML response to client
function send_response(response,top_ten_genres) {
	const top_genres = 10;
	response.send(`<!DOCTYPE html>
		<html lang="de">
		<head>
			<meta charset="UTF-8">
			<meta name="viewport" content="width=device-width, initial-scale=1.0">
			<title>Musik Genres</title>
			<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/mini.css/3.0.1/mini-default.min.css">
			<script>
				function fetchRandomMissions() {
					const maxRepetitions = Math.floor(Math.random() * 200)
					document.getElementById("out").innerText = "Fetching " + maxRepetitions + " random missions, see console output"
					for(var i = 0; i < maxRepetitions; ++i) {
						const missionId = Math.floor(Math.random() * 10)
						console.log("Fetching mission id " + missionId)
						fetch("/missions/sts-" + missionId, {cache: 'no-cache'})
					}
				}
			</script>
		</head>
		<body>
			<h1>Musik Genres</h1>
			<p>
				<a href="javascript: fetchRandomMissions();">Randomly fetch some missions</a>
				<span id="out"></span>
			</p>
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


function send_response_genre(response,userid, data) {

	response.send(`<!DOCTYPE html>
		<html lang="de">
		<head>
			<meta charset="UTF-8">
			<meta name="viewport" content="width=device-width, initial-scale=1.0">
			<title>Musik Genres</title>
			<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/mini.css/3.0.1/mini-default.min.css">
			<script>

			</script>
		</head>
		<body>
			<h1>Musik Genre: ${userid}</h1>
			<p>
				${data}
			</p>
			<a href="/">Zurück zur Startseite</a>

<hr>
			<h2>Informationen zu der generierten Seite</h2>
			<ul>
				<li>Host ${os.hostname()}</li>
				<li>Date: ${new Date()}</li>
				<li>Memcached Servers: ${memcachedServers}</li>
				<li>Result: <b>${userid}</b></li>
			</ul>
			</body>
	</html>`);
}




// Redirect / to person with ID l.mlb.com - p.7491
//response.writeHead(302, { 'Location': 'genre/pop' })
// datenbank - 10 beliebsten
app.get('/',  async function (request, response) {
	//Promise.all([getFromDatabase_start(),getFromDatabaseStartpage_popular()]).then(values => {
	Promise.all([getFromDatabase_start(),getFromDatabaseStartpage_popular()]).then(values => {
		const genres = values[0]
		const popular = values[1]

	const genre_html = genres.map(m => `<a href='/genre/${m.genre}'>${m.genre}</a>`)
			.join(", ")
	const popularHtml = popular
			.map(pop => `<li> <a href='/genre/${pop.genre}'>${pop.genre}</a> (${pop.count} views) </li>`)
			.join("\n")
	const html = `
			<h1>Top 10 Genres</h1>
			<p>
				<ol style="margin-left: 2em;"> ${popularHtml} </ol>
			</p>
			<h1>Alle Genres</h1>
			<p> ${genre_html} </p>`

	send_response(response,html)
		});
	//response.end();
})

// Get data about a single person
// app.getAsync('/genre/:id', async function (request, response) {
app.getAsync('/genre/:id', async function (request, response) {
	let userid = request.params["id"]
	let key =  userid
	let cachedata = await getFromCache(key)


	if (cachedata) {
		console.log(`Cache hit for key=${key}, cachedata = ${cachedata}`)
		send_response_genre(response,userid ,cachedata);
	} else {
		console.log(`Cache miss for key=${key}, querying database`)
		let data= await getFromDatabase_genre(userid)
		if (data) {
			console.log(`Got data=${data}, storing in cache`)
			//console.log(`Got tweet=${description}, storing in cache`)
			if (memcached)
				await memcached.set(key, data, 30 /* seconds */);
			send_response_genre(response,userid ,data);
		} else {
			send_response_genre(response,userid ,"No data found");
		}
	}
})




// Add stress test endpoint, cf. https://github.com/bermi/inefficient
app.get('/stress', inefficient);

// Set port to start the app on
app.set('port', (process.env.PORT || 8080))

// Start the application
app.listen(app.get('port'), function () {
	console.log("Node app is running at localhost:" + app.get('port'))
})
