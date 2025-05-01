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
  IonCardTitle,
  IonSearchbar
} from '@ionic/angular/standalone';
import { FormsModule } from '@angular/forms';
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
    IonContent,
    IonCard,
    IonCardContent,
    IonCardHeader,
    IonCardSubtitle,
    IonCardTitle,
    IonSearchbar,
    FormsModule    
  ]
})
export class ViewPage implements OnInit {
  items: Producto[] = [];
  filteredItems: Producto[] = [];
  searchTerm: string = '';

  filterItems() {
    const term = this.searchTerm.toLowerCase();
    if (!term) {
      this.filteredItems = this.items;
    } else {
      this.filteredItems = this.items.filter(item =>
        item.nom_producto.toLowerCase().includes(term) ||
        item.descripcion.toLowerCase().includes(term)
      );
    }
  }

  constructor(private apiService: APIService) { }

  ngOnInit() {
    const productos = localStorage.getItem('productos');
    if (productos && JSON.parse(productos).length > 0) {
      this.items = JSON.parse(productos);
      this.filteredItems = this.items; // <--- agrega esto
      console.log('Datos desde LS');
      console.log(this.items);
    } else {
      this.apiService.getdata().subscribe({
        next: (productos: Producto[]) => {
          this.items = productos;
          this.filteredItems = this.items; // <--- agrega esto
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