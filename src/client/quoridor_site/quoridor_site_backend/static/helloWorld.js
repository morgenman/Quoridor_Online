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
  // Logic for full screen image. Keep the frame square
  let image = this.add.image(config.width / 2, config.height / 2, 'bg');
  let scaleX = this.cameras.main.width / image.width
  let scaleY = this.cameras.main.height / image.height
  let scale = Math.max(scaleX, scaleY)
  image.setScale(scale).setScrollFactor(0)

  // Drawing starts from center, not top left of object, so this should be useful
  let center = { x: config.width / 2, y: config.height / 2 + 6 }


  let tile_size = config.width / 12.45;



  for (let i = -4; i <= 4; i++) {
    for (let j = -4; j <= 4; j++) {
      this.add.rectangle(center.x + i * tile_size, center.y + j * tile_size, tile_size - 2, tile_size - 2, 0x000000 + 0x100000 * (i + 4) + 0x001000 * (j + 4), 0.5);
    }
  }

  // var r3 = this.add.rectangle((config.width / 2), (config.height / 2), config.width - (2 * tile_size), config.height - (2 * tile_size), 0x4d8dcd79);

  // this.tweens.add({

  //   targets: r3,
  //   alpha: 0.2,


  // });


  // var r4 = this.add.rectangle(200, 400, 148, 148, 0xff6699);

  // var r5 = this.add.rectangle(400, 400, 148, 148, 0xff33cc);

  // var r6 = this.add.rectangle(600, 400, 148, 148, 0xff66ff);

  // this.tweens.add({

  //   targets: r4,
  //   scaleX: 0.25,
  //   scaleY: 0.5,
  //   yoyo: true,
  //   repeat: -1,
  //   ease: 'Sine.easeInOut'

  // });

  // this.tweens.add({

  //   targets: r5,
  //   alpha: 0.2,
  //   yoyo: true,
  //   repeat: -1,
  //   ease: 'Sine.easeInOut'

  // });

  // this.tweens.add({

  //   targets: r6,
  //   angle: 90,
  //   yoyo: true,
  //   repeat: -1,
  //   ease: 'Sine.easeInOut'

  // });
}
