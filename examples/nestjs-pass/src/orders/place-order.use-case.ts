import { Injectable } from "@nestjs/common";

@Injectable()
export class PlaceOrderUseCase {
  execute(): string {
    return "ok";
  }
}
