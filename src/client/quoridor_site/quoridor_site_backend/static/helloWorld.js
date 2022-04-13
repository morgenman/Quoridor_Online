import Phaser from 'phaser';
//import BoardPlugin from 'rexboardplugin.min.js';

var config = {
  type: Phaser.AUTO,
  parent: 'phaser-example',
  width: 800,
  height: 800,
  scene: {
    preload: preload,
    create: create
  }
};

var game = new Phaser.Game(config);

function preload() {
  console.log('Current directory: ' + process.cwd());
  this.load.image('bg', '/static/Board.png');
}

function create() {
  let image = this.add.image(config.width / 2, config.height / 2, 'bg');
  let scaleX = this.cameras.main.width / image.width
  let scaleY = this.cameras.main.height / image.height
  let scale = Math.max(scaleX, scaleY)
  image.setScale(scale).setScrollFactor(0)

  let grid_x = config.width * 0.2
  let grid_y = config.height * 0.2
  let tile_size = config.width / 15
  console.log("grid_x: " + grid_x)
  console.log("grid_y: " + grid_y)
  console.log("tile_size: " + tile_size)


  var r1 = this.add.rectangle(grid_x, grid_y, tile_size, tile_size, 0x6666ff);
  var r2 = this.add.rectangle(config.width - grid_x - tile_size, config.height - grid_y - tile_size, tile_size, tile_size, 0x6666ff);

  var r3 = this.add.rectangle((config.width / 2), (config.height / 2), config.width - (2 * tile_size), config.height - (2 * tile_size), 0x4d8dcd79);

  this.tweens.add({

    targets: r3,
    alpha: 0.2,


  });


  var r4 = this.add.rectangle(200, 400, 148, 148, 0xff6699);

  var r5 = this.add.rectangle(400, 400, 148, 148, 0xff33cc);

  var r6 = this.add.rectangle(600, 400, 148, 148, 0xff66ff);

  this.tweens.add({

    targets: r4,
    scaleX: 0.25,
    scaleY: 0.5,
    yoyo: true,
    repeat: -1,
    ease: 'Sine.easeInOut'

  });

  this.tweens.add({

    targets: r5,
    alpha: 0.2,
    yoyo: true,
    repeat: -1,
    ease: 'Sine.easeInOut'

  });

  this.tweens.add({

    targets: r6,
    angle: 90,
    yoyo: true,
    repeat: -1,
    ease: 'Sine.easeInOut'

  });
}
