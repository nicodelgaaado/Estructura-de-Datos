enum EstadoPedido {
    Solicitado = "Solicitado",
    EnPreparacion = "En preparación",
    Listo = "Listo",
    Servido = "Servido",
    Pagado = "Pagado"
}

class Pedido {
    constructor(
        public id: number,
        public cliente: string,
        public detalle: string[],
        public total: number = 0,
        public estado: EstadoPedido = EstadoPedido.Solicitado
    ) { }

    actualizarEstado(nuevoEstado: EstadoPedido): void {
        console.log(`Pedido ${this.id}: estado cambiado de ${this.estado} a ${nuevoEstado}`);
        this.estado = nuevoEstado;
    }
}

class Cliente {
    constructor(public nombre: string) { }

    solicitarPedido(mesero: Mesero, detalle: string[]): Pedido {
        console.log(`${this.nombre} solicita pedido: ${detalle.join(", ")}`);
        return mesero.recogerPedido(this.nombre, detalle);
    }

    solicitarCuenta(mesero: Mesero, pedido: Pedido) {
        console.log(`${this.nombre} solicita la cuenta`);
        mesero.solicitarCuenta(pedido);
    }

    pagarPedido(caja: Caja, pedido: Pedido) {
        console.log(`${this.nombre} procede a pagar`);
        caja.procesarPago(pedido);
    }
}

class Mesero {
    private pedidos: Pedido[] = [];

    recogerPedido(nombreCliente: string, detalle: string[]): Pedido {
        const pedido = new Pedido(
            Math.floor(Math.random() * 10000),
            nombreCliente,
            detalle
        );
        this.pedidos.push(pedido);
        console.log(`Mesero recoge pedido del cliente ${nombreCliente}`);
        Cocina.elaborarPedido(pedido);
        return pedido;
    }

    servirPedido(pedido: Pedido) {
        if (pedido.estado !== EstadoPedido.Listo) {
            console.log(`El pedido aún no está listo para servir`);
            return;
        }
        pedido.actualizarEstado(EstadoPedido.Servido);
        console.log(`Mesero sirve el pedido al cliente ${pedido.cliente}`);
    }

    solicitarCuenta(pedido: Pedido) {
        console.log(`Mesero solicita cuenta para el pedido ${pedido.id}`);
        Caja.calcularTotal(pedido);
    }
}

class Cocina {
    static elaborarPedido(pedido: Pedido) {
        pedido.actualizarEstado(EstadoPedido.EnPreparacion);
        console.log(`Cocina preparando pedido ${pedido.id}...`);
        setTimeout(() => {
            pedido.actualizarEstado(EstadoPedido.Listo);
            console.log(`Cocina: pedido ${pedido.id} está listo`);
        }, 2000);
    }
}

class Caja {
    static calcularTotal(pedido: Pedido) {
        pedido.total = pedido.detalle.length * 10;
        console.log(`Caja calcula total: $${pedido.total} para pedido ${pedido.id}`);
    }

    procesarPago(pedido: Pedido) {
        if (pedido.estado !== EstadoPedido.Servido) {
            console.log(`No se puede pagar hasta que se sirva el pedido`);
            return;
        }
        pedido.actualizarEstado(EstadoPedido.Pagado);
        console.log(`Caja: pedido ${pedido.id} pagado correctamente por $${pedido.total}`);
    }
}

class Restaurante {
    mesero: Mesero = new Mesero();
    caja: Caja = new Caja();

    nuevoCliente(nombre: string): Cliente {
        return new Cliente(nombre);
    }
}

const restaurante = new Restaurante();
const cliente1 = restaurante.nuevoCliente("Juan");

const pedidoJuan = cliente1.solicitarPedido(restaurante.mesero, ["Pizza", "Refresco"]);

setTimeout(() => {
    restaurante.mesero.servirPedido(pedidoJuan);
    cliente1.solicitarCuenta(restaurante.mesero, pedidoJuan);

    setTimeout(() => {
        cliente1.pagarPedido(restaurante.caja, pedidoJuan);
    }, 500);
}, 2500);
