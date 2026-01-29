import sys
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


def date_part(timestamp: str) -> str:
  """Return YYYY/MM/DD from YYYY/MM/DD-hh:mm:ss."""
  return timestamp.split("-")[0]


@dataclass
class Item:
  name: str
  cost: int
  list_price: int
  active: bool = True
  sales_sum: int = 0
  cost_sum: int = 0

  @property
  def margin(self) -> float:
    return 0.0 if self.sales_sum == 0 else (self.sales_sum - self.cost_sum) / self.sales_sum


@dataclass
class Seller:
  name: str
  sales_sum: int = 0
  cost_sum: int = 0

  @property
  def margin(self) -> float:
    return 0.0 if self.sales_sum == 0 else (self.sales_sum - self.cost_sum) / self.sales_sum


@dataclass
class Permit:
  seller_id: int
  item_id: int
  price: int
  date: str
  valid: bool = True


class System:
  def __init__(self, rate: float, sellers: List[str]) -> None:
    self.rate = rate
    self.sellers: Dict[int, Seller] = {i + 1: Seller(name) for i, name in enumerate(sellers)}
    self.items: Dict[int, Item] = {}
    self.item_name_to_id: Dict[str, int] = {}
    self.permits: Dict[int, Permit] = {}
    self.active_permit_by_seller: Dict[int, int] = {}
    self.next_item_id = 1
    self.next_permit_id = 1

  def register_item(self, ts: str, name: str, cost: int, list_price: int) -> str:
    if name in self.item_name_to_id:
      return "register-item: duplicated item"
    if list_price < cost:
      return "register-item: too cheap price"
    item_id = self.next_item_id
    self.next_item_id += 1
    self.items[item_id] = Item(name=name, cost=cost, list_price=list_price)
    self.item_name_to_id[name] = item_id
    return f"register-item: {item_id}"

  def request_sale(self, ts: str, seller_id: int, item_id: int, price: int) -> str:
    item = self.items.get(item_id)
    if not item or not item.active:
      return "request-sale: no such item"
    if seller_id not in self.sellers:
      return "request-sale: unauthorized operation"
    # price checks
    if price > item.list_price:
      return "request-sale: too expensive price"

    if price < item.list_price:
      # simulate margins
      seller = self.sellers[seller_id]
      new_s_sales = seller.sales_sum + price
      new_s_cost = seller.cost_sum + item.cost
      seller_margin = 0.0 if new_s_sales == 0 else (new_s_sales - new_s_cost) / new_s_sales

      new_i_sales = item.sales_sum + price
      new_i_cost = item.cost_sum + item.cost
      item_margin = 0.0 if new_i_sales == 0 else (new_i_sales - new_i_cost) / new_i_sales

      if price < item.cost or seller_margin < self.rate or item_margin < self.rate:
        return "request-sale: too cheap price"

    # approve permit
    permit_id = self.next_permit_id
    self.next_permit_id += 1
    # invalidate previous active permit of this seller
    old_pid = self.active_permit_by_seller.get(seller_id)
    if old_pid:
      self.permits[old_pid].valid = False
    permit = Permit(seller_id=seller_id, item_id=item_id, price=price, date=date_part(ts))
    self.permits[permit_id] = permit
    self.active_permit_by_seller[seller_id] = permit_id
    return f"request-sale: {permit_id}"

  def complete_sale(self, ts: str, seller_id: int, permit_id: int) -> str:
    permit = self.permits.get(permit_id)
    if not permit:
      return "complete-sale: no such sale"
    if permit.seller_id != seller_id:
      return "complete-sale: unauthorized operation"
    if not permit.valid:
      return "complete-sale: permission expired"
    if date_part(ts) != permit.date:
      permit.valid = False
      self.active_permit_by_seller.pop(seller_id, None)
      return "complete-sale: permission expired"

    item = self.items.get(permit.item_id)
    if not item or not item.active:
      permit.valid = False
      self.active_permit_by_seller.pop(seller_id, None)
      return "complete-sale: no such item"

    # finalize
    permit.valid = False
    self.active_permit_by_seller.pop(seller_id, None)
    seller = self.sellers[seller_id]
    seller.sales_sum += permit.price
    seller.cost_sum += item.cost
    item.sales_sum += permit.price
    item.cost_sum += item.cost
    return "complete-sale: ok"

  def delete_item(self, ts: str, item_id: int) -> str:
    item = self.items.get(item_id)
    if not item or not item.active:
      return "delete-item: no such item"
    # check active permits referencing item
    for pid, p in self.permits.items():
      if p.item_id == item_id and p.valid:
        return "delete-item: sales in progress"
    item.active = False
    self.item_name_to_id.pop(item.name, None)
    return "delete-item: ok"

  def update_item(self, ts: str, item_id: int, new_price: int) -> str:
    item = self.items.get(item_id)
    if not item or not item.active:
      return "update-item: no such item"
    if new_price < item.cost:
      return "update-item: too cheap price"
    for pid, p in self.permits.items():
      if p.item_id == item_id and p.valid:
        return "update-item: sales in progress"
    item.list_price = new_price
    return "update-item: ok"

  def get_margin_sellers(self, k: Optional[int] = None) -> List[str]:
    sellers_sorted = sorted(
        self.sellers.items(),
        key=lambda kv: (-kv[1].margin, kv[0])
    )
    lines = [f"get-margin-sellers:"] if k is None else [f"get-margin-sellers: {k}"]
    count = len(sellers_sorted) if k is None else min(k, len(sellers_sorted))
    for i in range(count):
      sid, s = sellers_sorted[i]
      lines.append(f"{sid} {s.name} {s.margin:.3f}")
    return lines

  def get_margin_items(self, k: Optional[int] = None) -> List[str]:
    items_sorted = sorted(
        ((iid, it) for iid, it in self.items.items() if it.active or it.sales_sum > 0),
        key=lambda kv: (-kv[1].margin, kv[0])
    )
    lines = [f"get-margin-items:"] if k is None else [f"get-margin-items: {k}"]
    count = len(items_sorted) if k is None else min(k, len(items_sorted))
    for i in range(count):
      iid, it = items_sorted[i]
      lines.append(f"{iid} {it.name} {it.margin:.3f}")
    return lines


def parse_query(line: str) -> Tuple[str, List[str]]:
  if ":" in line:
    cmd, rest = line.split(":", 1)
    parts = rest.strip().split()
    return cmd.strip(), parts
  return line.strip(), []


def main():
  data = [l.rstrip("\r\n") for l in sys.stdin if l.strip() != ""]
  if not data:
    return
  idx = 0
  rate = float(data[idx]); idx += 1
  seller_count = int(data[idx]); idx += 1
  sellers = []
  for _ in range(seller_count):
    sellers.append(data[idx].strip())
    idx += 1
  q = int(data[idx]); idx += 1
  system = System(rate, sellers)
  outputs: List[str] = []
  for _ in range(q):
    cmd, parts = parse_query(data[idx])
    idx += 1
    if cmd == "register-item":
      ts, name, cost, list_price = parts[0], parts[1], int(parts[2]), int(parts[3])
      outputs.append(system.register_item(ts, name, cost, list_price))
    elif cmd == "request-sale":
      ts, seller_id, item_id, price = parts[0], int(parts[1]), int(parts[2]), int(parts[3])
      outputs.append(system.request_sale(ts, seller_id, item_id, price))
    elif cmd == "complete-sale":
      ts, seller_id, permit_id = parts[0], int(parts[1]), int(parts[2])
      outputs.append(system.complete_sale(ts, seller_id, permit_id))
    elif cmd == "delete-item":
      ts, item_id = parts[0], int(parts[1])
      outputs.append(system.delete_item(ts, item_id))
    elif cmd == "update-item":
      ts, item_id, new_price = parts[0], int(parts[1]), int(parts[2])
      outputs.append(system.update_item(ts, item_id, new_price))
    elif cmd == "get-margin-sellers":
      k = int(parts[0]) if parts else None
      outputs.extend(system.get_margin_sellers(k))
    elif cmd == "get-margin-items":
      k = int(parts[0]) if parts else None
      outputs.extend(system.get_margin_items(k))
  sys.stdout.write("\n".join(outputs))


if __name__ == "__main__":
  main()
