import Phaser from 'phaser';
//import BoardPlugin from 'rexboardplugin.min.js';

var config = {
  type: Phaser.AUTO,
  parent: 'phaser-example',
  width: 800,
  height: 800,
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
  this.anims.create(p1_idle_config);
  this.anims.create(p2_idle_config);

  let p1 = this.add.sprite(center.x + (0 * tile_size), center.y + ((4) * tile_size) - 15, 'p1_idle').play('p1_idle_animation');
  let p2 = this.add.sprite(center.x + (0 * tile_size), center.y + ((-4) * tile_size) - 15, 'p2_idle').play('p2_idle_animation');
  p1.setScale(2);
  p2.setScale(2);





  for (let i = 0; i < 9; i++) {
    for (let j = 0; j < 9; j++) {
      this.add.rectangle(center.x + (i - 4) * tile_size, center.y + (j - 4) * tile_size, tile_size - 2, tile_size - 2, 0x000000 + 0x100000 * i + 0x001000 * j, 0.5);
    }
  }






}
