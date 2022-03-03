# DAC8568(WIP)

## Description

DAC8568是一个8通道、16位精度的数模转换器，兼容`SPI`, `QSPI`, `Microwave`和`DSP`接口。

## Features

1. 给指定通道施加指定的电压
2. 设置使用内部参考电压
2. 设置使用外部参考电压

## Example

```python
from machine import SPI, Pin
import dac8568

# define spi/cs, esp32-s for example
spi = SPI(2, 10000)
cs = machine.Pin(5, Pin.OUT)

# init dac8568
dac8568_ = dac8568.DAC8568(spi, cs)

# use internal reference
dac8568_.use_internal_reference()

# set voltage
dac8568_.set_voltage(dac8568.Channel.A, 65535)
```

## Reference

- [rust version](https://github.com/ostenning/dac8568)
- [data sheet](https://www.ti.com.cn/product/cn/DAC8568)

