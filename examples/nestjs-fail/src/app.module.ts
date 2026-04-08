import { Module } from "@nestjs/common";

import { CommonHelper } from "./orders/common-helper";
import { OrderManager } from "./orders/order-manager";
import { UserRepository } from "./orders/user-repository";

@Module({
  providers: [OrderManager, UserRepository, CommonHelper],
})
export class AppModule {}
