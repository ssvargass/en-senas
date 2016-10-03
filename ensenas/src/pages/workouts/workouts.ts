import { Component,NgZone } from '@angular/core';
import { Camera } from 'ionic-native';
import { NavController } from 'ionic-angular';
import * as io from "socket.io-client";

@Component({
  selector: 'page-workouts',
  templateUrl: 'workouts.html'
})

export class WorkoutsPage {
  imageSrc: string;
  socketHost: string = 'http://192.168.0.18:8000/'; 
  socket: any;
  zone: any;
  result: string;
  
  constructor(public navCtrl: NavController) { 
    this.zone = new NgZone({enableLongStackTrace: false});
    this.socket = io.connect(this.socketHost);
    this.socket.emit('my message', 'something', (data => this.result = data)); 
  }

  openGallery(){
    let cameraOptions = {
      sourceType: Camera.PictureSourceType.PHOTOLIBRARY,
      destinationType: Camera.DestinationType.DATA_URL,      
      quality: 100,
      targetWidth: 1000,
      targetHeight: 1000,
      encodingType: Camera.EncodingType.JPEG,      
      correctOrientation: true
    }

    Camera.getPicture(cameraOptions)
      .then(imageData => this.processImage(imageData), 
      err => console.log(err));   
  }

  takePicture(){
    let cameraOptions = {
        destinationType: Camera.DestinationType.DATA_URL,
        targetWidth: 1000,
        targetHeight: 1000,
        encodingType: Camera.EncodingType.JPEG, 
    }

    Camera.getPicture(cameraOptions)
      .then(imageData => this.processImage(imageData),
      (err) => console.log(err));
  }

  processImage(imageData){
    this.imageSrc = "data:image/jpeg;base64," + imageData;
    this.socket.emit('my message', imageData, (data => this.result = data));
  }


}
