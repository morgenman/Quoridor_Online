import Phaser from 'phaser';
//import BoardPlugin from 'rexboardplugin.min.js';

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
  scene: {
    preload: preload,
    create: create
  }

};

var game = new Phaser.Game(config);



function preload() {
  console.log('Current directory: ' + process.cwd());
  this.load.image('bg', '/static/Board.png');
  this.load.spritesheet('p1_idle', '/static/P1_Idle.png', { frameWidth: 64, frameHeight: 64, endFrame: 1 });
  this.load.spritesheet('p2_idle', '/static/P2_Idle.png', { frameWidth: 64, frameHeight: 64, endFrame: 1 });
  this.load.spritesheet('p3_idle', '/static/P3_Idle.png', { frameWidth: 64, frameHeight: 64, endFrame: 1 });
  this.load.spritesheet('p4_idle', '/static/P4_Idle.png', { frameWidth: 64, frameHeight: 64, endFrame: 1 });
  this.load.spritesheet('h_wall', '/static/h_wall.png', { frameWidth: 192, frameHeight: 64, endFrame: 0 });
  this.load.spritesheet('v_wall', '/static/v_wall.png', { frameWidth: 64, frameHeight: 192, endFrame: 0 });

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
  console.log('Shorthand: ' + state);
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
        let p1 = this.add.sprite(coor.x, coor.y - 15, 'p1_idle').play('p1_idle_animation');
        p1.setScale(2);
        break;
      case 1: // Player 2
        let p2 = this.add.sprite(coor.x, coor.y - 15, 'p2_idle').play('p2_idle_animation');
        p2.setScale(2);
        break;
      case 2: // Player 3
        let p3 = this.add.sprite(coor.x, coor.y - 15, 'p3_idle').play('p3_idle_animation');
        p3.setScale(2);
        break;
      case 3: // Player 4
        let p4 = this.add.sprite(coor.x, coor.y - 15, 'p4_idle').play('p4_idle_animation');
        p4.setScale(2);
    }
  }

  var h_walls = (String(temp[0]).trim()).match(/.{2}/g);
  for (var wall in h_walls) {
    var strng = h_walls[wall].split("");
    x = String(strng[0]).charCodeAt(0) - 96; //gives you the number of the letter. 
    y = strng[1]; // y position
    console.log("making h wall: " + x + "; y: " + y);
    let coor = coor_2_abs(x, y);
    let h_wall_1 = this.add.sprite(coor.x, coor.y - 40, 'h_wall');
    h_wall_1.setScale(1.2);
  }
  var v_walls = (String(temp[1]).trim()).match(/.{2}/g);
  console.log(h_walls + ";" + v_walls);
  var x = 0;
  var y = 0;
  for (var wall in v_walls) {
    var strng = v_walls[wall].split("");
    x = String(strng[0]).charCodeAt(0) - 96; //gives you the number of the letter. 
    y = strng[1]; // y position
    let coor = coor_2_abs(x, y);

    console.log("making v_wall from '", wall, "' at " + x + "," + y);
    let v_wall_1 = this.add.sprite(coor.x + 40, coor.y, 'v_wall');
    v_wall_1.setScale(1.2);
  }


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

  

  //movable target object
  var target = this.add.sprite(900, 900, 'target').setInteractive();
  target.setScale(0.5);

  //gives green tint when pointer is over target
  this.input.topOnly = false;
  target.on('pointerover', function () {

    this.setTint(0x00ff00);
  });

  //undoes above
  target.on('pointerout', function () {

    this.clearTint();

  });

  this.input.setDraggable(target);

  //gives red tint when being dragged
  this.input.on('dragstart', function (pointer, gameObject) {

    gameObject.setTint(0xff0000);

  });

  //controls dragging
  this.input.on('drag', function (pointer, gameObject, dragX, dragY) {

    gameObject.x = dragX;
    gameObject.y = dragY;

  });

  //undoes tint when drag ends
  this.input.on('dragend', function (pointer, gameObject) {

    gameObject.clearTint();

  });

  function coor_2_abs(x, y) {
    return {
      x: center.x + (x - 5) * tile_size,
      y: center.y + (-1 * (y - 5) * tile_size)
    }
  }




}
