ar request = require("request");
var Q = require("q")
var aws = require('aws-sdk');
var url = "https://s3-eu-west-1.amazonaws.com/xxxxxxxx/list.json" // S3 URL with JSON
var webs;

// function to get JSON with URL
function getJSON(url)
{
    var params={
        method: 'GET',
        timeout: 100, // Timeout miliseconds
        uri: url
    };     
    return Q.nfcall(request, params);
}

// Function to save all URL in promises
function process_json(data)
{
    webs=JSON.parse(data[0].body);
    
    promises = [];
    webs["URLs"].forEach(function(web){ 
        promises.push(Q.npost(request, web.method , [web.url], web.params))
    });

    return Q.allSettled(promises);
}

// Function to process all URL
function process(results)
{
    var i=0;
    
     results.forEach(function (result) {
        if (result.state === "fulfilled") {
            if(result.value[0].statusCode!=200){
                console.log("WebPage Error, " + webs.URLs[i].url + " is down")
                sendSNS(webs.URLs[i].url);
            }

        } else {
            console.log("WebPage Error, " + webs.URLs[i].url + " is down")
            sendSNS(webs.URLs[i].url);            
        }
        i++;
    });  
}

// Fucntion to send SNS with Error.
function sendSNS(URL)
{
    var sns = new aws.SNS({
        region: 'eu-west-1' 

    });
    var params = {
        TopicArn: "SNS ARN TOPI" // Include your ARN
    };
    params.Subject = "WebPage Error, " + URL + "is down"
    params.Message = "WebPage Error, " + URL + "is down"
    sns.publish(params, function(err, data) {
        if(err) {
            console.error('error publishing to SNS', err);
        } else {
            console.info('message published to SNS', data);
        }
    });
}

exports.handler = function(event, context) {

    // Promises
    Q(url)
        .then(getJSON)
        .then(process_json)
        .then(process)
        .catch(function(err) {context.fail(err);})
        .finally(function() {context.done(null, "OK");})
        .done();
}
