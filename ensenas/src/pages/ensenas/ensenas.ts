/// <reference path="../../../typings/globals/socket.io-client/index.d.ts" />
import { Component,NgZone } from '@angular/core';
import { Camera } from 'ionic-native';
import { NavController } from 'ionic-angular';
import * as io from "socket.io-client";

@Component({
  selector: 'page-ensenas',
  templateUrl: 'ensenas.html'
})

export class EnsenasPage {
  imageSrc: string;
  socketHost: string = 'http://104.236.17.92:8000/'; 
  socket: any;
  zone: any;
  results: any;
  
  constructor(public navCtrl: NavController) { 
    this.zone = new NgZone({enableLongStackTrace: false});
    this.socket = io.connect(this.socketHost);
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
    this.socket.emit('my message', imageData, ((data) => {
      this.results = eval(data);
    }));
  }


}
