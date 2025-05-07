import { Component, OnInit } from '@angular/core';
import {
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
  IonButton,
  IonIcon,
  IonSelect,
  IonSelectOption,
  AlertController,
  ToastController,
  ActionSheetController
} from '@ionic/angular/standalone';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { APIService, Producto } from 'src/app/services/api.service';
import { addIcons } from 'ionicons';
import { search, pencil, removeCircle } from 'ionicons/icons';
import { firstValueFrom } from 'rxjs';

@Component({
  selector: 'app-view',
  templateUrl: './view.page.html',
  styleUrls: ['./view.page.scss'],
  standalone: true,
  imports: [
    CommonModule,
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
    IonButton,
    IonIcon,
    IonSelect,
    IonSelectOption,
    FormsModule
  ]
})
export class ViewPage implements OnInit {
  items: Producto[] = [];
  filteredItems: Producto[] = [];
  searchTerm: string = '';
  showNoResultsMessage: boolean = false;
  sortOption: string = '';

  constructor(
    private apiService: APIService,
    private toastController: ToastController,
    private alertController: AlertController,
    private actionSheetController: ActionSheetController
  ) {
    addIcons({ search, pencil, removeCircle });
  }

  ngOnInit() {
    const productos = localStorage.getItem('productos');
    if (productos && JSON.parse(productos).length > 0) {
      this.items = JSON.parse(productos);
      this.filteredItems = this.items;
    } else {
      this.apiService.getdata().subscribe({
        next: (productos: Producto[]) => {
          this.items = productos;
          this.filteredItems = this.items;
          localStorage.setItem('productos', JSON.stringify(this.items));
        },
        error: (err) => {
          console.error('Error al cargar productos:', err);
        }
      });
    }
  }

  async mostrarMensaje(mensaje: string, color: string = 'danger') {
    const toast = await this.toastController.create({
      message: mensaje,
      duration: 2000,
      color: color,
      position: 'middle'
    });
    toast.present();
  }

  filterItems() {
    const term = this.searchTerm.toLowerCase().trim();

    if (!term) {
      this.filteredItems = this.items;
      this.showNoResultsMessage = false;
    } else {
      this.filteredItems = this.items.filter(item =>
        item.nom_producto.toLowerCase().includes(term) ||
        item.descripcion.toLowerCase().includes(term) ||
        String(item.cod_material).toLowerCase().includes(term)
      );

      if (this.filteredItems.length === 0) {
        this.filteredItems = this.items;
        this.showNoResultsMessage = true;
      } else {
        this.showNoResultsMessage = false;
      }
    }

    this.sortItems(); // Ordenar después de filtrar
  }

  onSearchbarChange() {
    const term = this.searchTerm.toLowerCase().trim();
    if (!term) {
      this.mostrarMensaje('Por favor, ingrese un texto para buscar.');
    }
  }

  sortItems() {
    if (!this.sortOption) {
      return;
    }
    this.filteredItems.sort((a, b) => {
      switch (this.sortOption) {
        case 'nombre':
          return a.nom_producto.localeCompare(b.nom_producto);
        case 'categoria':
          return a.categoria_id.toString().localeCompare(b.categoria_id.toString());
        case 'cantidad':
          return a.cant_existencia - b.cant_existencia;
        default:
          return 0;
      }
    });
  }

  // NUEVO: Mostrar Action Sheet con opciones Editar/Eliminar cantidad
  async abrirMenuProducto(producto: Producto) {
    const actionSheet = await this.actionSheetController.create({
      header: `Acciones para "${producto.nom_producto}"`,
      buttons: [
        {
          text: 'Eliminar existencia',
          icon: 'remove-circle',
          handler: () => {
            this.abrirVentanaEliminarCantidad(producto);
          }
        },
        {
          text: 'Editar',
          icon: 'create-outline',
          handler: () => {
            this.mostrarMensaje('Funcionalidad de edición pendiente.', 'primary');
          }
        },
        {
          text: 'Cancelar',
          icon: 'close',
          role: 'cancel'
        }
      ]
    });
    await actionSheet.present();
  }

  // Ventana para eliminar cantidad
  async abrirVentanaEliminarCantidad(producto: Producto) {
    const alert = await this.alertController.create({
      header: `Eliminar Existencia de "${producto.nom_producto}"`,
      inputs: [
        {
          name: 'existencia',
          type: 'number',
          min: 1,
          max: producto.cant_existencia,
          placeholder: 'Existencia a eliminar',
        }
      ],
      buttons: [
        {
          text: 'Cancelar',
          role: 'cancel'
        },
        {
          text: 'Listo',
          handler: (data) => {
            const cantidad = parseInt(data.cantidad, 10);
            if (!cantidad || cantidad < 1 || cantidad > producto.cant_existencia) {
              this.mostrarMensaje('Cantidad inválida', 'danger');
              return false; // Evita que el alert se cierre
            }
            this.confirmarEliminarCantidad(producto, cantidad);
            return true; // <- Aquí el fix: retorna true para cerrar el alert
          }
        }
      ]
    });
    await alert.present();
  }

  // Segunda confirmación
  async confirmarEliminarCantidad(producto: Producto, cantidad: number) {
    const alert = await this.alertController.create({
      header: '¿Seguro?',
      message: `¿Deseas eliminar ${cantidad} unidades de "${producto.nom_producto}"?`,
      buttons: [
        {
          text: 'Cancelar',
          role: 'cancel'
        },
        {
          text: 'Sí, eliminar',
          handler: () => {
            this.restarCantidadProducto(producto.cod_material, cantidad);
          }
        }
      ]
    });
    await alert.present();
  }

  // Lógica para restar cantidad
  restarCantidadProducto(cod_material: number, cantidad: number) {
    this.apiService.restarCantidad(cod_material, cantidad).subscribe({
      next: () => {
        // Actualiza localmente el stock
        const prod = this.items.find(p => p.cod_material === cod_material);
        if (prod) {
          prod.cant_existencia -= cantidad;
        }
        this.filterItems();
        this.mostrarMensaje('Cantidad eliminada exitosamente', 'success');
      },
      error: () => {
        this.mostrarMensaje('No se pudo eliminar la cantidad', 'danger');
      }
    });
  }
}
