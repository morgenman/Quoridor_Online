import Phaser from 'phaser';
var interactive = true;
var global_board = "";
let delay = 5000;
var p1;
var p2;
var p3;
var p4;

let timerId = setTimeout(function request() {
  var board = document.getElementById('state');
  console.log('Requesting...');
  try {
    board = refreshBoard();
  }
  catch (error) {
    console.log(error);
    // increase the interval to the next run
    delay *= 2;
  }
  Promise.resolve(board).then(function (board) {
    document.getElementById('state').value = board;
  });

  timerId = setTimeout(request, delay);

}, delay);


function update() {
  if (global_board != document.getElementById('state').value) {
    global_board = document.getElementById('state').value;
    console.log("Changed global board");
    let scaleX = this.cameras.main.width / 2048
    let scaleY = this.cameras.main.height / 2048
    let scale = Math.max(scaleX, scaleY)
    // Drawing starts from center, not top left of object, so this should be useful
    let center = { x: config.width / 2, y: config.height / 2 + 6 }
    let tile_size = config.width / 12.45;
    var x = 0;
    var y = 0;
    var shorthand = document.getElementById('state').value;
    console.log('Shorthand: ' + shorthand.text);
    var temp = shorthand.split("/");
    var play_piece = (String(temp[2]).trim()).split(" ");
    for (var i = 0; i < play_piece.length; i++) {
      var end = play_piece[i].split("");
      x = String(end[0]).charCodeAt(0) - 96; //gives you the number of the letter. 
      y = end[1]; // y position   
      console.log("player: " + i + "; x: " + x + "; y: " + y);
      let coor = coor_2_abs(x, y);
      switch (i) {
        case 0: // Player 1
          p1.destroy();
          p1 = this.add.sprite(coor.x, coor.y - 15, 'p1_idle').play('p1_idle_animation');
          //p1.setScale(2);
          p1.setInteractive({ pixelPerfect: true });
          this.input.setDraggable(p1);
          break;
        case 1: // Player 2
          p2.destroy();
          p2 = this.add.sprite(coor.x, coor.y - 15, 'p2_idle').play('p2_idle_animation');
          //p2.setScale(2);
          p2.setInteractive({ pixelPerfect: true });
          this.input.setDraggable(p2);
          break;
        case 2: // Player 3
          p3.destroy();
          p3 = this.add.sprite(coor.x, coor.y - 15, 'p3_idle').play('p3_idle_animation');
          //p3.setScale(2);
          p3.setInteractive({ pixelPerfect: true });
          this.input.setDraggable(p3);
          break;
        case 3: // Player 4
          p4.destroy();
          p4 = this.add.sprite(coor.x, coor.y - 15, 'p4_idle').play('p4_idle_animation');
          //p4.setScale(2);
          p4.setInteractive({ pixelPerfect: true });
          this.input.setDraggable(p4);
      }
    }
    function coor_2_abs(x, y) {
      return {
        x: center.x + (x - 5) * tile_size,
        y: center.y + (-1 * (y - 5) * tile_size)
      }
    }

    function abs_2_coor(x, y) {
      return {
        x: Math.floor((x - center.x) / tile_size) + 6,
        y: Math.floor((-1 * (y - center.y)) / tile_size) + 5
      }
    }
  }

}




class h_wall_sprite extends Phaser.GameObjects.Sprite {
  constructor(scene, x, y, name) {
    if (name === 'h_wall') {
      super(scene, x, y - 40, name);
      this.setInteractive(new Phaser.Geom.Rectangle(84, 28, 60, 16), Phaser.Geom.Rectangle.Contains);

    }
    else if (name === 'v_wall') {
      super(scene, x + 40, y, name);
      //this.setScale(1.2);
      this.setInteractive(new Phaser.Geom.Rectangle(28, 84, 16, 60), Phaser.Geom.Rectangle.Contains);
    }
    this.visible = false;
    this.on('pointerover', function (pointer) {
      if (interactive) this.visible = true;
    });
    this.on('pointerout', function (pointer) {
      if (interactive) this.visible = false;
    });

    this.input.topOnly = true;
    this.input.alwaysEnabled = true;
    this.setAlpha(0.5);

    this.on('pointerdown', function (pointer) {
      if (interactive) {
        this.setInteractive(false);
        this.visible = true;
        this.setAlpha(1);
      }
    });
  }
}

class CustomPlugin extends Phaser.Plugins.BasePlugin {

  constructor(pluginManager) {
    super(pluginManager);
    //  Register our new Game Object type
    pluginManager.registerGameObject('h_wall_sprite', this.createHWall, this);
  }

  createHWall(x, y, name) {
    return this.displayList.add(new h_wall_sprite(this.scene, x, y, name));
  }

}


var config = {
  type: Phaser.AUTO,
  parent: 'board',
  width: 1000,
  height: 1000,
  scale: {
    // Or set parent divId here
    parent: 'board',

    mode: Phaser.Scale.FIT,
    autoCenter: Phaser.Scale.CENTER_BOTH,

    // Or put game size here
    // width: 1024,
    // height: 768,

    // Minimum size
    min: {
      width: 50,
      height: 50
    },
    // Or set minimum size like these
    // minWidth: 800,
    // minHeight: 600,

    // Maximum size
    max: {
      width: 1600,
      height: 1600
    },
    // Or set maximum size like these
    // maxWidth: 1600,
    // maxHeight: 1200,

    zoom: 1,  // Size of game canvas = game size * zoom
  },
  autoRound: false,
  antialias: false,
  plugins: {
    global: [
      { key: 'CustomPlugin', plugin: CustomPlugin, start: true }
    ]
  },
  scene: {
    preload: preload,
    create: create,
    update: update
  }

};

var game = new Phaser.Game(config);



function preload() {
  this.load.image('bg', '/static/Board.png');
  this.load.spritesheet('p1_idle', '/static/P1_Idle.png', { frameWidth: 128, frameHeight: 128, endFrame: 1 });
  this.load.spritesheet('p2_idle', '/static/P2_Idle.png', { frameWidth: 128, frameHeight: 128, endFrame: 1 });
  this.load.spritesheet('p3_idle', '/static/P3_Idle.png', { frameWidth: 128, frameHeight: 128, endFrame: 1 });
  this.load.spritesheet('p4_idle', '/static/P4_Idle.png', { frameWidth: 128, frameHeight: 128, endFrame: 1 });
  this.load.spritesheet('h_wall', '/static/h_wall.png', { frameWidth: 230, frameHeight: 77, endFrame: 0 });
  this.load.spritesheet('v_wall', '/static/v_wall.png', { frameWidth: 77, frameHeight: 230, endFrame: 0 });

  this.load.image('target', '/static/Target.png');

}


function create() {
  // Logic for full screen image. Keep the frame square
  let image = this.add.image(config.width / 2, config.height / 2, 'bg');
  let scaleX = this.cameras.main.width / image.width
  let scaleY = this.cameras.main.height / image.height
  let scale = Math.max(scaleX, scaleY)
  image.setScale(scale).setScrollFactor(0)


  // Drawing starts from center, not top left of object, so this should be useful
  let center = { x: config.width / 2, y: config.height / 2 + 6 }
  let tile_size = config.width / 12.45;

  this.data.set('coordinates', "x,y");
  let coor = coor_2_abs(0, 10);
  var text = this.add.text(coor.x, coor.y, '', { font: '30px IBM Plex Mono', fill: '#00ff00' });
  text.setText(this.data.get('coordinates'));

  // Players
  var p1_idle_config = {
    key: 'p1_idle_animation',
    frames: this.anims.generateFrameNumbers('p1_idle', { start: 0, end: 1, first: 0 }),
    frameRate: 2,
    repeat: -1
  };
  var p2_idle_config = {
    key: 'p2_idle_animation',
    frames: this.anims.generateFrameNumbers('p2_idle', { start: 0, end: 1, first: 0 }),
    frameRate: 2,
    repeat: -1
  };
  var p3_idle_config = {
    key: 'p3_idle_animation',
    frames: this.anims.generateFrameNumbers('p3_idle', { start: 0, end: 1, first: 0 }),
    frameRate: 2,
    repeat: -1
  };
  var p4_idle_config = {
    key: 'p4_idle_animation',
    frames: this.anims.generateFrameNumbers('p4_idle', { start: 0, end: 1, first: 0 }),
    frameRate: 2,
    repeat: -1
  };

  this.anims.create(p1_idle_config);
  this.anims.create(p2_idle_config);
  this.anims.create(p3_idle_config);
  this.anims.create(p4_idle_config);

  //Player pieces 
  var x = 0;
  var y = 0;
  var shorthand = document.getElementById('state').value;
  console.log('Shorthand: ' + shorthand.text);
  var temp = shorthand.split("/");
  var play_piece = (String(temp[2]).trim()).split(" ");
  for (var i = 0; i < play_piece.length; i++) {
    var end = play_piece[i].split("");
    x = String(end[0]).charCodeAt(0) - 96; //gives you the number of the letter. 
    y = end[1]; // y position   
    console.log("player: " + i + "; x: " + x + "; y: " + y);
    let coor = coor_2_abs(x, y);
    switch (i) {
      case 0: // Player 1
        p1 = this.add.sprite(coor.x, coor.y - 15, 'p1_idle').play('p1_idle_animation');
        //p1.setScale(2);
        p1.setInteractive({ pixelPerfect: true });
        this.input.setDraggable(p1);
        break;
      case 1: // Player 2
        p2 = this.add.sprite(coor.x, coor.y - 15, 'p2_idle').play('p2_idle_animation');
        //p2.setScale(2);
        p2.setInteractive({ pixelPerfect: true });
        this.input.setDraggable(p2);
        break;
      case 2: // Player 3
        p3 = this.add.sprite(coor.x, coor.y - 15, 'p3_idle').play('p3_idle_animation');
        //p3.setScale(2);
        p3.setInteractive({ pixelPerfect: true });
        this.input.setDraggable(p3);
        break;
      case 3: // Player 4
        p4 = this.add.sprite(coor.x, coor.y - 15, 'p4_idle').play('p4_idle_animation');
        //p4.setScale(2);
        p4.setInteractive({ pixelPerfect: true });
        this.input.setDraggable(p4);
    }
  }


  var banned_walls = [];

  let temp_h_wall = [];
  let temp_v_wall = [];
  var h_walls = (String(temp[0]).trim()).match(/.{2}/g);
  for (var wall in h_walls) {
    var strng = h_walls[wall].split("");
    x = String(strng[0]).charCodeAt(0) - 96; //gives you the number of the letter. 
    y = strng[1]; // y position
    temp_h_wall.push({ x: x, y: parseInt(y) });
    temp_h_wall.push({ x: x + 1, y: parseInt(y) });
    temp_h_wall.push({ x: x - 1, y: parseInt(y) });
    temp_v_wall.push({ x: x, y: parseInt(y) });
    console.log("making h wall: " + x + "; y: " + y);
    let coor = coor_2_abs(x, y);
    let h_wall_1 = this.add.sprite(coor.x, coor.y - 40, 'h_wall');
    //h_wall_1.setScale(1.2);
  }

  var v_walls = (String(temp[1]).trim()).match(/.{2}/g);
  console.log(h_walls + ";" + v_walls);
  for (var wall in v_walls) {
    var strng = v_walls[wall].split("");
    x = String(strng[0]).charCodeAt(0) - 96; //gives you the number of the letter. 
    y = strng[1]; // y position
    temp_v_wall.push({ x: x, y: parseInt(y) });
    temp_v_wall.push({ x: x, y: parseInt(y) + 1 });
    temp_v_wall.push({ x: x, y: parseInt(y) - 1 });
    temp_h_wall.push({ x: x, y: parseInt(y) });
    let coor = coor_2_abs(x, y);

    console.log("making v_wall from '", wall, "' at " + x + "," + y);
    let v_wall_1 = this.add.sprite(coor.x + 40, coor.y, 'v_wall');
    //v_wall_1.setScale(1.2);
  }
  banned_walls.push(temp_h_wall);
  banned_walls.push(temp_v_wall);


  //This handles the potential moves
  var highlight = " e2f1d1 "
  var active_tiles = (String(highlight).trim()).match(/.{2}/g);
  var x = 0;
  var y = 0;
  for (var tile in active_tiles) {
    var strng = active_tiles[tile].split("");
    x = String(strng[0]).charCodeAt(0) - 96; //gives you the number of the letter. 
    y = strng[1]; // y position
    let coor = coor_2_abs(x, y);

    this.add.rectangle(coor.x, coor.y, tile_size - 2, tile_size - 2, 0x00FF08, 0.3);
  }

  // Rainbow Grid
  // for (let i = 1; i <= 9; i++) {
  //   for (let j = 1; j <= 9; j++) {
  //     let coor = coor_2_abs(i, j);
  //     this.add.rectangle(coor.x, coor.y, tile_size - 2, tile_size - 2, 0x000000 + 0x100000 * i + 0x001000 * j, 0.5);
  //   }
  // }

  console.log(banned_walls);

  for (let i = 1; i <= 8; i++) {
    for (let j = 1; j <= 8; j++) {
      let coor = coor_2_abs(i, j);
      if (!banned_walls[0].filter(function (e) { return (e.x === i) && (e.y === j); }).length > 0) {
        var sprite = this.add.h_wall_sprite(coor.x, coor.y, 'h_wall');
        //this.input.enableDebug(sprite);
      }
      coor = coor_2_abs(j, i);
      if (!banned_walls[1].filter(function (e) { return (e.x === j) && (e.y === i); }).length > 0) {
        var sprite = this.add.h_wall_sprite(coor.x, coor.y, 'v_wall');
        //this.input.enableDebug(sprite, 0x0000FF);
      }
    }

  }









  this.input.topOnly = false;



  //gives red tint when being dragged
  this.input.on('dragstart', function (pointer, gameObject) {
    interactive = false;
    gameObject.setTint(0xff0000);

  });

  //controls dragging
  this.input.on('drag', function (pointer, gameObject, dragX, dragY) {

    gameObject.x = dragX;
    gameObject.y = dragY;
    let coor = abs_2_coor(dragX - gameObject.width / 4, dragY - gameObject.height / 4);
    text.setText(coor.x + "," + coor.y);

  });

  //undoes tint when drag ends
  this.input.on('dragend', function (pointer, gameObject) {
    interactive = true;
    gameObject.clearTint();

    let xy = abs_2_coor(gameObject.x - gameObject.width / 4, gameObject.y - gameObject.height / 4);
    let coor = coor_2_abs(xy.x, xy.y);
    gameObject.x = coor.x;
    gameObject.y = coor.y - 15;
    text.setText(xy.x + "," + xy.y);

  });

  function coor_2_abs(x, y) {
    return {
      x: center.x + (x - 5) * tile_size,
      y: center.y + (-1 * (y - 5) * tile_size)
    }
  }

  function abs_2_coor(x, y) {
    return {
      x: Math.floor((x - center.x) / tile_size) + 6,
      y: Math.floor((-1 * (y - center.y)) / tile_size) + 5
    }
  }





}
async function refreshBoard() {
  var id = document.getElementById('game-id').value;
  const response = await fetch("http://localhost:9696/get", {
    method: "POST",
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ "id": id })
  })
  return response.text();
}
