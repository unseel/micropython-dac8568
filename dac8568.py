from micropython import const

class Channel:
  """Channel Enum."""

  A = const(0x00)
  B = const(0x01)
  C = const(0x02)
  D = const(0x03)
  E = const(0x04)
  F = const(0x05)
  G = const(0x06)
  H = const(0x07)

class Control:
  """Control Enum."""
  WriteToInputRegister = const(0x00)
  WriteToChannelAndUpdateAllRegisters = const(0x2)
  WriteToChannelAndUpdateSingleRegister = const(0x03) # 00000011
  InternalReferenceStatic = const(0x08) # 00001000

class Feature:
  """Feature Enum."""

  InternalReference = const(0x00)
  ExternalReference = const(0x01)

class Payload:
  """Data Input Register Format"""

  def __init__(self):
    self.prefix = const(0x00) # 4bits
    self.control = const(0x00) # 4bits
    self.address = const(0x00) # 4bits
    self.data = const(0x00) # 16bits
    self.feature = const(0x00) # 4bits
  
  def set_control(self, control):
    self.control = control
  
  def set_address(self, address):
    self.address = address

  def set_data(self, data):
    self.data = data

  def set_feature(self, feature):
    self.feature = feature
  
  def to_bytes(self):
    result = 0
    result = result | self.prefix << 28
    result = result | self.control << 24
    result = result | self.address << 20
    result = result | self.data << 4
    result = result | self.feature << 0
    return result.to_bytes(4, 'big')

class DAC8568:
  """Implementation for dac8568"""

  def __init__(self, spi, cs):
    self.spi = spi
    self.cs = cs
  
  def use_internal_reference(self):
    payload:Payload = Payload()
    payload.set_control(Control.InternalReferenceStatic)
    payload.set_feature(Feature.InternalReference)
    self.__write__(payload)

  def use_external_reference(self):
    payload:Payload = Payload()
    payload.set_control(Control.InternalReferenceStatic)
    payload.set_feature(Feature.ExternalReference)
    self.__write__(payload)

  """set voltage to specified channel"""
  def set_voltage(self, channel, voltage):
    payload:Payload = self.set_voltage0(channel, voltage)
    payload.set_control(Control.WriteToInputRegister)
    self.__write__(payload)

  """set voltage to specified channel, and update"""
  def set_and_update_voltage(self, channel, voltage):
    payload:Payload = self.set_voltage0(channel, voltage)
    payload.set_control(Control.WriteToChannelAndUpdateSingleRegister)
    self.__write__(payload)
  
  """set voltage to specified channel, and update all"""
  def set_and_update_all_voltage(self, channel, voltage):
    payload:Payload = self.set_voltage0(channel, voltage)
    payload.set_control(Control.WriteToChannelAndUpdateAllRegisters)
    self.__write__(payload)

  def set_voltage0(self, channel, voltage):
    voltage = self.check_voltage(voltage)
    payload:Payload = Payload()
    payload.set_address(channel)
    payload.set_data(voltage)
    return payload
  
  def check_voltage(self, voltage):
    if voltage < 0:
      voltage = 0
    if voltage > 65535:
      voltage = 65535
    return voltage

  def __write__(self, payload):
    self.cs.off()
    result = self.spi.write(payload.to_bytes())
    print(result)
    self.cs.on()

if __name__ == '__main__':
  payload = Payload()
  payload.set_control(Control.WriteToChannelAndUpdateSingleRegister)
  payload.set_address(Channel.A)
  payload.set_data(65535)
  print(payload.to_bytes())
