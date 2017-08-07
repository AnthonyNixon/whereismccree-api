/**
 * Responds to any HTTP request that can provide a "message" field in the body.
 *
 * @param {!Object} req Cloud Function request context.
 * @param {!Object} res Cloud Function response context.
 */

const googleapis = require('googleapis');
var request = require('request');

exports.getMcreeLocation = function getMcreeLocation(req, res) {
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Headers", "X-Requested-With");


    UTCHour = new Date().getUTCHours();
    UTCMinute = new Date().getUTCMinutes();

    if (UTCMinute >= 30) {
        UTCHour++;
    }

    console.log(UTCHour);

    hourDiff = 12 - UTCHour;


    if (hourDiff >= 0) {
        filename = 'UTC+' + hourDiff + '_00.txt';
    } else {
        filename = 'UTC' + hourDiff + '_00.txt';
    }


    request.get('https://storage.googleapis.com/location-by-utc-offset/'+filename, function (error, response, body) {
        if (!error && response.statusCode === 200) {
            var locationList = body;
            console.log({"locations": locationList});
            // Continue with your processing here.
            var locations = locationList.split('\n');
            locations.pop();
            console.log(locations);

            location = locations[Math.floor(Math.random()*locations.length)];
            res.status(200).send(location);
        } else {
            console.error('Problem getting location file from storage bucket');
            res.status(500).send('error getting location file ' + filename);
        }
    });
};