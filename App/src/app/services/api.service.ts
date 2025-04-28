import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators'; // Corrección en la importación

export interface Producto {
  cod_material: number;
  nom_producto: string;
  cant_existencia: number;
  descripcion: string;
  stock_minimo: number;
  stock_maximo: number;
  categoria_id: number;
}

@Injectable({
  providedIn: 'root'
})
export class APIService {
  url = "http://127.0.0.1:8000/rest/v1/producto";

  constructor(private http: HttpClient) { }

  getdata(): Observable<Producto[]> {
    return this.http.get<{ data: Producto[] }>(this.url).pipe(
      map(response => response.data)
    );
  } // Cierre correcto del método
}
