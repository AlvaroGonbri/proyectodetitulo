
import { JsonPipe } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import {
  IonHeader, 
  IonToolbar, 
  IonTitle, 
  IonContent, // <-- Importa IonContent
  IonCard, 
  IonCardContent, 
  IonCardHeader, 
  IonCardSubtitle, 
  IonCardTitle 
} from '@ionic/angular/standalone';
import { APIService, Producto } from 'src/app/services/api.service';

@Component({
  selector: 'app-view',
  templateUrl: './view.page.html',
  styleUrls: ['./view.page.scss'],
  standalone: true,
  imports: [
    IonHeader,
    IonToolbar,
    IonTitle,
    IonContent, // <-- Agrega IonContent aquí
    IonCard,
    IonCardContent,
    IonCardHeader,
    IonCardSubtitle,
    IonCardTitle,
    JsonPipe
  ]
})
export class ViewPage implements OnInit {
  items: Producto[] = [];

  constructor(private apiService: APIService) { }

  ngOnInit() {
    // Intenta cargar desde localStorage solo si hay datos
    const productos = localStorage.getItem('productos');
    if (productos && JSON.parse(productos).length > 0) {
      this.items = JSON.parse(productos);
      console.log('Datos desde LS');
      console.log(this.items);
    } else {
      // Si no hay datos en LS, consulta la API
      this.apiService.getdata().subscribe({
        next: (productos: Producto[]) => {
          this.items = productos;
          localStorage.setItem('productos', JSON.stringify(this.items));
          console.log('datos desde API');
          console.log(this.items);
        },
        error: (err) => {
          console.error('Error al cargar productos:', err);
        }
      });
    }
  }
}
