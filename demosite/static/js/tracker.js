// 1. Page visit count
// 2. User ip address
// 3. User browser
// 4. User operating system
// 5. User device
// 6. User country
// 7. User city
// 8. User region
// 9. User latitude
// 10. User longitude
// 11. duration of visit

common_url = 'http://192.168.18.146:8000'

fetch('https://api.ipify.org/?format=json')
.then(response => response.json())
.then(data => {
    ip = data.ip;
    console.log(ip);
    addCookie("ip", ip, 1);
});


function addCookie(name, value, days) {
    var expires;
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toGMTString();
    }
    else {
        expires = "";
    }
    document.cookie = escape(name) + "=" + escape(value) + expires + "; path=/";
}



//User browser
function fnBrowserDetect(){
    
    let userAgent = navigator.userAgent;
    let browserName;
    
    if(userAgent.match(/chrome|crios/i)){
        browserName = "Chrome";
    }else if(userAgent.match(/firefox|fxios/i)){
        browserName = "Firefox";
    }else if(userAgent.match(/safari/i)){
        browserName = "Safari";
    }else if(userAgent.match(/opr\//i)){
    browserName = "Opera";
}else if(userAgent.match(/edg/i)){
    browserName = "Edge";
}else{
    browserName="No browser detection";
}
return browserName;
}
//For user operating system

function getOs(){
    var OSName="Unknown OS";
    if (navigator.userAgent.indexOf("Win")!=-1) OSName="Windows";
    if (navigator.userAgent.indexOf("Mac")!=-1) OSName="MacOS";
    if (navigator.userAgent.indexOf("X11")!=-1) OSName="UNIX";
    if (navigator.userAgent.indexOf("Linux")!=-1) OSName="Linux";
    return OSName;
}
//For user device
function getUserDevice(){
    var device="Unknown Device";
    if (navigator.userAgent.indexOf("Mobile")!=-1) device="Mobile";
    if (navigator.userAgent.indexOf("Tablet")!=-1) device="Tablet";
    if (navigator.userAgent.indexOf("Linux")!=-1) device="Desktop";
    if (navigator.userAgent.indexOf("iPad")!=-1) device="Tablet";
    if (navigator.userAgent.indexOf("iPhone")!=-1) device="Mobile";
    if (navigator.userAgent.indexOf("Android")!=-1) device="Mobile";
    if (navigator.userAgent.indexOf("Windows")!=-1) device="Desktop";
    if (navigator.userAgent.indexOf("Mac")!=-1) device="Desktop";
    if (navigator.userAgent.indexOf("Desktop")!=-1) device="Desktop";
    if(navigator.userAgent.indexOf("Laptop")!=-1) device="Laptop";
    
    return device;
}



//For user data
function getDetails(){
    $.getJSON("https://ipapi.co/json/", function(data) {
    lat = data.latitude;
    long = data.longitude;
    city = data.city;
    region = data.region;
    country = data.country_name;
    console.log(`Country: ${country} City: ${city} Region: ${region}`);
    console.log(`Latitude: ${lat} Longitude: ${long}`);
});
}



//For duration of visit
function setDuration(){
    var startTime = new Date().getTime();
    // store start time in cookie
    addCookie("start", startTime, 1);
    // when tab is closed store end time in cookie
    window.onbeforeunload = function() {
        var endTime = new Date().getTime();
        addCookie("end", endTime, 1);
    }
}

function getDuration(){
    //cookie = document.cookie;
    //cookie = cookie.split(";");
    //console.log(cookie);
    end = document.cookie.split(";").filter(c => c.indexOf("end") >= 0)[0].split("=")[1]
    start = document.cookie.split(";").filter(c => c.indexOf("start") >= 0)[0].split("=")[1]
    duration = Math.abs(end - start);
    return formatTime(duration);
}

function formatTime(ms) {
    return Math.floor(ms / 1000);
}

// contact form submission


function track_registration(e){
    let ip = document.cookie.split(";").filter(c => c.indexOf("ip") >= 0)[0].split("=")[1];
    post_url = common_url +'/track/register'
    console.log("sending register form submission data")
    console.log(ip);
    $.ajax({
        type: "POST",
        url: post_url,
        datatype: "jsonp",
        data: {
            "ip": ip,
            "website": $(location).attr('href'),
        },
        success: function (data) {
            console.log("sent register form submission data")
            console.log(data);
            
        },
        error: function (data) {
            console.log('An error occurred.');
            console.log(data);
        },
        crossDomain: true,
    });
}

function track_logins(e){
    // get ip from cookie
    //let ip = document.cookie.split(";").filter(c => c.indexOf("ip") >= 0)[0].split("=")[1];
    post_url = common_url+'/track/logins'
    console.log("sending login form submission data")
    console.log(ip);
    $.ajax({
        type: "POST",
        url: post_url,
        datatype: "jsonp",
        data: {
            "ip": ip,
            "website": $(location).attr('href'),
        },
        success: function (data) {
            console.log("sent login form submission data")
            console.log(data);
            
        },
        error: function (data) {
            console.log('An error occurred.');
            console.log(data);
        },
        crossDomain: true,
    });
}

// function visitCounter(ip){
//     addCookie("ip", ip, 1);
//     // check if visit cookie exists
//     console.log(document.cookie.indexOf("visit"));
//     if (document.cookie.indexOf("visit") >= 0) {
//         // if exists, get the value
//         document.cookie.split(";").forEach(function(c) {
//             if (c.indexOf("visit") >= 0) {
//                 visit = c.split("=")[1];
//             }
//         });
//         // increment the value
//         visit++;
//         // store the new value
//         addCookie("visit", visit, 1);
//     }   
// }

function getIp(){
    $.getJSON("https://api.ipify.org?format=jsonp&callback=?",
    function(json) {
        console.log("IP Address: "+json.ip);
        addCookie("ip", json.ip, 1);
        out = visitCounter(json.ip);
        console.log(out);
        console.log("Browser: " + fnBrowserDetect());
        console.log("OS: " + getOs());
        console.log("Device: " + getUserDevice());
        // getDetails();
        console.log(`Duration: ${getDuration()} seconds`)
        //getDuration();
    });
}

function save_contact_form_data(e){
    let ip = document.cookie.split(";").filter(c => c.indexOf("ip") >= 0)[0].split("=")[1];
    post_url = common_url + '/track/contacts'
    console.log("sending contact form submission data")
    console.log(ip);
    $.ajax({
        type: "POST",
        url: post_url,
        datatype: "jsonp",
        data: {
            "ip": ip,
            "website": $(location).attr('href'),
        },
        success: function (data) {
            console.log("sent contact form submission data")
            console.log(data);
            // redirect to home
            //window.location.href = "/";
        },
        error: function (data) {
            console.log('An error occurred.');
            console.log(data);
        },
        crossDomain: true,
    });
}


function track_page_visits(){
    // get ip from cookie
    let ip = document.cookie.split(";").filter(c => c.indexOf("ip") >= 0)[0].split("=")[1];
    post_url = common_url + '/track/pagevists'
    console.log(ip)
    console.log("sending page visit data " + ip)
    $.ajax({
        type: "POST",
        url: post_url,
        datatype: "jsonp",
        data: {
            "ip": ip,
            "website": $(location).attr('href'),
            
        },
        success: function (data) {
            console.log("sent page visit data")
            console.log(data);
            
        },
        error: function (data) {
            console.log('An error occurred.');
            console.log(data);
        },
        crossDomain: true,
    });
}


// display in console
setDuration()
//visitCounter()

//getIp()

//track page visits
function page_data(){
    //let ip = document.cookie.split(";").filter(c => c.indexOf("ip") >= 0)[0].split("=")[1];
    post_url = common_url + '/track/main'
    console.log("sending page data")
    fetch('https://ipapi.co/json/')
    .then(response => response.json())
    .then(data => {
        $.ajax({
            type: "POST",
            url: post_url,
            datatype: "jsonp",
            data: {
                "ip": data.ip,
                "website": $(location).attr('href'),
                "browser": fnBrowserDetect(),
                "os": getOs(),
                "device": getUserDevice(),
                "city": data.city,
                "region": data.region,
                "country": data.country,
                "lat": data.latitude,
                "long": data.longitude,
                "duration": getDuration(),
            },
            success: function (data) {
                console.log("sent page data")
                console.log(data);
                
            },
            error: function (data) {
                console.log('An error occurred.');
                console.log(data);
            },
            crossDomain: true,
            
            
        });
    }); 
}


