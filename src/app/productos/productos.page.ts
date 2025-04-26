import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-productos',
  templateUrl: './productos.page.html',
  styleUrls: ['./productos.page.scss'],
})
export class ProductosPage implements OnInit {
  categoriaId = 0;
  productos: any[] = [];

  data = [
    { cod_material: 1010, nom_producto: 'Martillo Carpintero', categoria_id: 1 },
    { cod_material: 1011, nom_producto: 'Destornillador Plano', categoria_id: 1 },
    { cod_material: 1012, nom_producto: 'Taladro Percutor Bosch', categoria_id: 2 },
  ];

  constructor(private route: ActivatedRoute) {}

  ngOnInit() {
    this.route.queryParams.subscribe(params => {
      this.categoriaId = +params['id'];
      this.productos = this.data.filter(p => p.categoria_id === this.categoriaId);
    });
  }
}
