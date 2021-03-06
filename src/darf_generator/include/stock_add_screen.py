#!/usr/bin/python3

from PySide2 import QtCore
from PySide2 import QtWidgets
from darf_generator.include.stock import Stock
from darf_generator.include.stock import StockTypes
from darf_generator.include.stock_add_ui import Ui_StockAdd

class StockAddScreen(QtWidgets.QWidget, Ui_StockAdd):

# Definition of Qt Signals
#----------------------------------------------------------------------------------------------------------------------
    exit_add_stock_signal = QtCore.Signal()
    add_stock_signal = QtCore.Signal(Stock)

# Constructor
#----------------------------------------------------------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        super(StockAddScreen, self).__init__()
        self.setupUi(self)
        self.__stock = Stock()
        self.totalValueLabel.setText("0.00")
        self.nameInput.textChanged.connect(self.on_name_changed)
        self.priceInput.valueChanged.connect(self.on_price_changed)
        self.ammountInput.valueChanged.connect(self.on_ammount_changed)
        self.saveButton.clicked.connect(self.on_save_button_clicked)
        self.backButton.clicked.connect(self.on_back_button_clicked)

# SLOT - Change title name when stock name changes
#----------------------------------------------------------------------------------------------------------------------  
    def on_name_changed(self, new_name):
        self.stockNameLabel.setText(new_name)

# SLOT - Change total price when price changed
#----------------------------------------------------------------------------------------------------------------------  
    def on_price_changed(self, new_price):
        self.totalValueLabel.setText("%0.2f" %(new_price * self.ammountInput.value()))

# SLOT - Change total price when ammount changed
#----------------------------------------------------------------------------------------------------------------------  
    def on_ammount_changed(self, new_ammount):
        self.totalValueLabel.setText("%0.2f" %(new_ammount * self.priceInput.value()))

# SLOT - Save the stock when user press the save button
#----------------------------------------------------------------------------------------------------------------------  
    def on_save_button_clicked(self):
        self.__stock.name = self.nameInput.text()
        self.__stock.price = self.priceInput.value()
        self.__stock.ammount = self.ammountInput.value()
        self.__stock.paid_fares = self.faresInput.value()
        self.__stock.category = StockTypes.FI if self.categoryInput.currentIndex() == 0 else StockTypes.NORMAL
        self.add_stock_signal.emit(self.__stock)

# SLOT - Fires when receive the update signal from the control
#----------------------------------------------------------------------------------------------------------------------
    @QtCore.Slot(str)
    def update_add_stock_slot(self, error_message):
        if error_message != "":
            self.errorLabel.setStyleSheet("color: red")
            self.errorLabel.setText(error_message)
        else:
            self.errorLabel.setStyleSheet("color: green")
            self.errorLabel.setText("Ação %s salva com sucesso!" %self.nameInput.text())
            self.nameInput.setText("")
            self.categoryInput.setCurrentIndex(1)
            self.priceInput.setValue(0.0)
            self.ammountInput.setValue(0)
            self.faresInput.setValue(0.0)

# SLOT - Process the back button clicked
#----------------------------------------------------------------------------------------------------------------------  
    def on_back_button_clicked(self):
        self.exit_add_stock_signal.emit()
