from abc import ABC, abstractmethod

class MetodoPagoInterface(ABC):
    @abstractmethod
    def procesar_pago(self, monto):
        """Procesa el pago con un monto dado."""
        pass
