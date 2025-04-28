import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { IonicModule } from '@ionic/angular';
import { ViewPageRoutingModule } from './view-routing.module';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    ViewPageRoutingModule
    // No agregues ViewPage aquí si es standalone
    // No agregues HttpClientModule aquí si ya está en AppModule
  ],
  // declarations: [], // No declares componentes standalone aquí
  // providers: [] // No es necesario para APIService si es providedIn: 'root'
})
export class ViewPageModule {}
