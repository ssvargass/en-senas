import { NgModule } from '@angular/core';
import { IonicApp, IonicModule } from 'ionic-angular';
import { MyApp } from './app.component';
import { TabsPage } from '../pages/tabs/tabs';
import { EnsenasPage } from '../pages/ensenas/ensenas';


@NgModule({
  declarations: [
    MyApp,
    TabsPage,
    EnsenasPage,
  ],
  imports: [
    IonicModule.forRoot(MyApp)
  ],
  bootstrap: [IonicApp],
  entryComponents: [
    MyApp,
    TabsPage,
    EnsenasPage,
  ],
  providers: []
})
export class AppModule {}
