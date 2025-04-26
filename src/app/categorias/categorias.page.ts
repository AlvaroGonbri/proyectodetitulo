import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-categorias',
  templateUrl: './categorias.page.html',
  styleUrls: ['./categorias.page.scss'],
})
export class CategoriasPage {
  categorias = [
    { id_categoria: 1, nom_categoria: 'Herramientas Manuales' },
    { id_categoria: 2, nom_categoria: 'Herramientas Eléctricas' },
    { id_categoria: 3, nom_categoria: 'Materiales de Construcción' },
    // Puedes agregar más si quieres
  ];

  constructor(private router: Router) {}

  verProductos(categoria: any) {
    this.router.navigate(['/productos'], { queryParams: { id: categoria.id_categoria } });
  }
}
