init offset = -1

init python:

    ## 인벤토리
    registered_items = {}
    item_list = []
    quest_dict = {}
    add1, add2, slot_count, what, output = "", "", 0, "", ""
    add_insert, insert_what = "", ""

    def find_item(id):
        return registered_items[id]

    class Item:
        def __init__(self, id, name):
            self.id = id
            self.name = name
            registered_items[id] = self
        
        def __hash__(self):
            return hash(self.id)

        def __eq__(self, other):
            return self.__class__ == other.__class__ and self.id == other.id

        def __reduce__(self):
            return find_item, (self.id, )
        
    class ItemStack:
        def __init__(self, item, count=1):
            self.item = item
            self.count = count
    
    class Inventory:
        def __init__(self):
            self._stacks = {}
            self._ordered = []
            self._global_count = 0

        def __len__(self):
            return len(self._ordered)

        @property
        def global_count(self):
            return self._global_count

        def add(self, item, count=1):
            if count < 1:
                raise ValueError("1보다 크거나 같아야 합니다.")
            stack = self.fetch_stack(item)
            stack.count += count
            self._global_count += count

        def remove(self, item, count=1):
            if count < 1:
                raise ValueError("1보다 크거나 같아야 합니다.")
            stack = self.fetch_stack(item)
            if stack is None:
                return

            remove_count = min(count, stack.count)
            stack.count -= remove_count
            self._global_count -= remove_count

            if stack.count <= 0:
                del self._stacks[item]
                self._ordered.remove(stack)
        
        def fetch_stack(self, item, require=True):
            stack = self._stacks.get(item, None)
            if stack is None:
                if not require:
                    return None
                self._stacks[item] = stack = ItemStack(item, 0)
                self._ordered.append(stack)
            # assert stack.count != 0
            return stack

        def __iter__(self):
            return iter(self._ordered)

    ## 제작
    class Craft:
        def __init__(self, item1, item2, result):
            self.item1 = item1
            self.item2 = item2
            self.result = result

        def slot(input):
            global add1
            global add2
            global slot_count

            if slot_count == 0:
                inven.remove(input, 1)
                add1 = inven.fetch_stack(input).item
                add2 = ""
                slot_count += 1
            elif slot_count == 1:
                inven.remove(input, 1)
                add1 = add1
                add2 = inven.fetch_stack(input).item
                slot_count += 1
            elif slot_count == 2:
                pass
            return

        def recipe(item1, item2, result):
            recipe_menu = [item1, item2, result]
            item_list.append(recipe_menu)
            return

        def crafting():
            global add1
            global add2
            global slot_count
            global what
            global output

            craftitem = 0
            
            for i in item_list:
                if add1 == "" or add2 == "":
                    what = "재료 부족"
                    return
                if i[0] == add1:
                    if i[1] == add2:
                        craftitem += 1
                        result = i[2]
                    else:
                        craftitem += 0
                elif i[1] == add1:
                    if i[0] == add2:
                        craftitem += 1
                        result = i[2]
                    else:
                        craftitem += 0
                else:
                    craftitem += 0
            
            if craftitem == 0:
                inven.add(add1, 1)
                inven.add(add2, 1)
                what = "제작 실패"
            else:
                inven.add(result, 1)
                output = result
                what = "제작 성공. [output.name] 획득"
            add1 = ""
            add2 = ""
            slot_count = 0
            return

    ## 퀘스트
    class Quest:
        def __init__(self, id, name):
            self.id = id
            self.name = name

        def add(id, name):
            quest_dict[id] = name

        def remove(id):
            del quest_dict[id]

    ## 아이템 투입
    class Insert:
        def __init__(self):
            self.item = item
            self.result = result
        
        def slot(input):
            global add_insert

            if add_insert == "":
                inven.remove(input, 1)
                add_insert = inven.fetch_stack(input).item
            else:
                pass
            return

        def check(result, success):
            global add_insert
            global insert_what

            if add_insert == result:
                insert_what = "투입 성공"
                add_insert = ""
                renpy.jump(success)
            elif add_insert == "":
                insert_what = "투입 없음"
            else:
                inven.add(add_insert, 1)
                insert_what = "투입 실패"
                add_insert = ""
            


            



    