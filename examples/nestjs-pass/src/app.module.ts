import { Module } from "@nestjs/common";

import { OrderController } from "./orders/order.controller";
import { PlaceOrderUseCase } from "./orders/place-order.use-case";

@Module({
  controllers: [OrderController],
  providers: [PlaceOrderUseCase],
})
export class AppModule {}
