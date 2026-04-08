import { Controller, Post } from "@nestjs/common";

import { PlaceOrderUseCase } from "./place-order.use-case";

@Controller("orders")
export class OrderController {
  constructor(private readonly placeOrderUseCase: PlaceOrderUseCase) {}

  @Post()
  placeOrder(): string {
    return this.placeOrderUseCase.execute();
  }
}
