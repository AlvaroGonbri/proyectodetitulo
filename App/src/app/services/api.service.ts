import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

export interface Producto {
  cod_material: number;
  nom_producto: string;
  cant_existencia: number;
  descripcion: string;
  stock_minimo: number;
  stock_maximo: number;
  categoria_id: number;
}

export interface Tecnico {
  id: number;
  nombre: string;
}

@Injectable({
  providedIn: 'root'
})
export class APIService {
  private baseUrl = "http://127.0.0.1:8000/rest/v1";
  private productoUrl = `${this.baseUrl}/producto`;

  constructor(private http: HttpClient) { }

  getdata(): Observable<Producto[]> {
    return this.http.get<{ data: Producto[] }>(this.productoUrl).pipe(
      map(response => response.data)
    );
  }

  // Verifica si el producto tiene movimientos/historial
  verificarMovimientosProducto(productoId: number): Observable<boolean> {
    return this.http.get<{ tiene_movimientos: boolean }>(
      `${this.productoUrl}/${productoId}/movimientos`
    ).pipe(map(response => response.tiene_movimientos));
  }

  // Elimina el producto
  eliminarProducto(productoId: number): Observable<any> {
    return this.http.delete(`${this.productoUrl}/${productoId}`);
  }
  restarCantidad(cod_material: number, cantidad: number): Observable<any> {
    return this.http.patch(`${this.productoUrl}/${cod_material}/restar_cantidad`, { cantidad });
  }
}
