// Function that gets the x and y from the shorthand and plots on the board. 
// Function that displays player pieces, horizontal and vertical walls, on the game board.
// horzontal walls / vertical walls / player pieces / correct tiles / incorrect tiles
var shorthand = "d4 f4 e7 / a2 a8 / e4 e6 a4 h6 / e5 a8 / a1 f1 / 4 3 5 3 / 3";

function displayPlayers(shorthand) {

    x_point = 0;
    y_point = 0;
    temp = shorthand.split("/");
    temp[0] = temp[0].trim();
    temp[1] = temp[1].trim();
    temp[2] = temp[2].trim();
    temp[3] = temp[3].trim();
    temp[4] = temp[4].trim();


    //Player pieces 
    var play_piece = temp[2].split(" ");
    for (var i = 0; i < play_piece.length; i++) {
        for (var k = 0; k < 2; k++) {
            var end = play_piece[i].split("");
            x_point = end[0]; // x position
            var n = x_point.charCodeAt(0) - 97; //gives you the number of the letter. 
            y_point = end[1]; // y position 
        }
        console.log(n + "," + y_point) // prints x and y coordinated for player pieces. ex. A 4 -> 0 4 ---> X Y 
        //this.add.rectangle(n * 100, y_point * 100, tile_size - 2, tile_size - 2, 0xff6699);  
    }
    //For Horizontal walls
    var h_walls = temp[0].split(" ");
    for (var i = 0; i < h_walls.length; i++) {
        for (var k = 0; k < 2; k++) {
            var fin = h_walls[i].split("");
            var xp = fin[0]; // x position
            var w = xp.charCodeAt(0) - 97; //gives you the number of the letter. 
            var y_p = fin[1]; // y position 

        }
        //console.log(w + "," + y_p)
        //this.add.rectangle(w * 100, y_point * 100, tile_size - 2, tile_size - 2, 0xff6699);  
    }
    //For Verticle walls
    var v_walls = temp[1].split(" ");
    for (var i = 0; i < v_walls.length; i++) {

        for (var k = 0; k < 2; k++) {
            var verti = v_walls[i].split("");
            var xp1 = verti[0]; // x position
            var v = xp1.charCodeAt(0) - 97; //gives you the number of the letter. 
            var yp1 = verti[1]; // y position 

        }
        //console.log(v + "," + yp1)
        //this.add.rectangle(w * 100, y_point * 100, tile_size - 2, tile_size - 2, 0xff6699);  
    }

}




display_pieces(shorthand);