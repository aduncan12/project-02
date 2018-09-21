// $(document).ready(function(){
//     $.ajax({
//         method: "GET",
//         url: "api/users/<int:pk>/preferences",
//         success:function(response){
//             console.log(response["preferences"])
//         },
//         error: function(error){
//             console.log(error)
//         }
//     })
// })
$(document).ready(function () {    
    $.ajax({
        method: "GET",
        url: "preferences",
        success: function (response) {
            var cuisines = response["preferences"].join('%2C');
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(function (position) {
                    var pos = {
                        lat: position.coords.latitude,
                        lng: position.coords.longitude
                    };
                    var my_url = `https://developers.zomato.com/api/v2.1/search?lat=${pos.lat}&lon=${pos.lng}&cuisines=${cuisines}`
                    console.log(my_url)
                    $.ajax({
                        url: my_url,
                        headers: {
                            "user-key": "f6e6a18b7e1f07fd9821453b651767fb"
                        },
                        method: 'GET',
                        dataType: 'json',
                        success: function (data) {
                            console.log(data)
                            console.log(data.restaurants)
                            var totalresults = data.restaurants;
                            if (totalresults.length > 0) {
                                var newArr = nRandEleArr(totalresults, 4);
                                console.log(newArr);
                                newArr.forEach(ele => {
                                    $('#restList').append(`
                                    <div>
                                    <p>Name: ${ele.restaurant.name}</p>
                                    <img src="${ele.restaurant.featured_image}" width="200em">
                                    <p>Cuisines: ${ele.restaurant.cuisines}</p>
                                    <p>Lat: ${ele.restaurant.location.latitude}, Lon: ${ele.restaurant.location.longitude}</p>
                                    </div>
                                    `);
                                    makeMarker(parseFloat(ele.restaurant.location.latitude), parseFloat(ele.restaurant.location.longitude), ele.restaurant.name);
                                });
                            } else {
                                $('#restList').append(`<h5>no results</h5>`);
                            }
                        }
                    });
                    return pos;
                });
            }
        },
        error: function (error) {
            console.log(error);
        }
    });
});

function nRandEleArr(arr, size) {
    var mySet = new Set();
    while (mySet.size < size) {
        mySet.add(arr[Math.floor(Math.random() * arr.length)]);
    }
    return [...mySet];
}

function makeMarker(lat, lng, name){
    L.marker([lat, lng]).addTo(map).bindPopup(`<b>${name}</b>`);
}
