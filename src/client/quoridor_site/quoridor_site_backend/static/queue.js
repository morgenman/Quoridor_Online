

var data = startQueue();
Promise.resolve(data).then(function (data) {
    document.getElementById('player-id').value = data['p1'];
    console.log(JSON.stringify(data))
    navigateToGame();
});
var delay = 10000;
let timerId = setTimeout(function request() {
    try {

        // console.log('Requesting...');
        // try {
        //     var data = startQueue();
        //     Promise.resolve(data).then(function (data) {
        //         console.log(JSON.stringify(data))
        //         if (data.ready) {
        //             document.getElementById('player-id').value = data['p1'];
        //             console.log("WOOOOOOO")
        //             navigateToGame();
        //             //window.location = './new_game'
        //         }
        //     });
        var p2_user_id = refreshQueue();

        Promise.resolve(p2_user_id).then(function (p2_user_id) {
            console.log("Im here");

            let p2_id = p2_user_id;
            if (p2_id.ready) {
                window.location = './game/' + p2_id.game_id;
            }
            else if (!p2_id.ready) {

                console.log("Not ready")
                var data = startQueue();
                Promise.resolve(data).then(function (data) {
                    if (data.ready) {
                        document.getElementById('player-id').value = data['p1'];
                        console.log(JSON.stringify(data))
                        navigateToGame();
                    }
                });
            }
        }
        )
    }
    catch (error) {
        console.log(error);
        // increase the interval to the next run
        delay *= 2;
    }


    timerId = setTimeout(request, delay);

}, delay);


async function refreshQueue() {
    var id = document.getElementById('player-id').value;
    const response = await fetch("http://localhost:9696/queue", {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ "player_id": id, "size": 2 })
    })
    return response.json();
}

async function startQueue() {
    var id = document.getElementById('player-id').value;
    const response = await fetch("http://localhost:9696/enqueue", {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ "player_id": id, "size": 2 })
    })
    return response.json();
}

async function navigateToGame() {
    var id = document.getElementById('player-id').value;
    document.sbmt.submit();


}