init python:
    registered_items = {}
    item_list = []
    add1, add2, slot_count, what, output = "", "", 0, "", ""

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
                    what = ""
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
            

    # 아이템 목록
    PLANT = Item('Plant', '식물')
    FLOWER = Item('Flower', '꽃')
    RIBBON = Item('Ribbon', '리본')
    BUG = Item('Bug', '벌레')

    # 조합 레시피
    Craft.recipe(PLANT, FLOWER, RIBBON)
    Craft.recipe(RIBBON, FLOWER, BUG)


screen inventory:
    
    frame:
        align (0.1, 0.5)
        xsize 500
        ysize 500

        vbox:
            vbox:
                text "보유 아이템 종류: %s" %(len(inven))
                text '인벤토리 총량: [inven.global_count]'
            
            viewport:
                draggable True
                mousewheel True
                xfill True
                yfill True

                scrollbars "vertical"

                vbox:
                    for stack in inven:
                        hbox:
                            if stack.count != 0:
                                textbutton "[stack.item.name]":
                                    xysize (300, 50)
                                    action Return(stack.item.id)
                                text "x[stack.count]"

    frame:
        align (0.6, 0.5)
        xsize 100
        ysize 100
        
        if add1 == "":
            $ name1 = ""
        else:
            $ name1 = add1.name

        textbutton "[name1]":
            xalign 0.5
            yalign 0.5
            action Return("Add1")

    frame:
        align (0.7, 0.5)
        xsize 100
        ysize 100

        if add2 == "":
            $ name2 = ""
        else:
            $ name2 = add2.name

        textbutton "[name2]":
            xalign 0.5
            yalign 0.5
            action Return("Add2")

    frame:
        align (0.65, 0.7)
        xsize 100
        ysize 100
        
        textbutton "◆":
            xalign 0.5
            yalign 0.5
            action Return("Craft")

screen craftsuccess:
    timer 1.0 action Hide("craftsuccess")
    frame:
        align (0.67, 0.3)
        xsize 300
        ysize 100

        text what:
            xalign 0.5
            yalign 0.5


label start:

    $ inven = Inventory()

    show screen inventory

    $ inven.add(FLOWER, 3)
    $ inven.add(RIBBON, 3)
    $ inven.add(PLANT, 3)

    $ end = False

    call screen inventory

    while end == False:

        if _return == "Add1":
            if slot_count == 1:
                $ inven.add(add1, 1)
                $ add1 = ""
                $ add2 = ""
                $ slot_count -= 1
            elif slot_count == 2:
                $ inven.add(add1, 1)
                $ add1 = add2
                $ add2 = ""
                $ slot_count -= 1
            else:
                pass
        elif _return == "Add2":
            if slot_count == 2:
                $ inven.add(add2, 1)
                $ add1 = add1
                $ add2 = ""
                $ slot_count -= 1
            else:
                pass
        elif _return == "Craft":
            $ Craft.crafting()
            show screen craftsuccess
        # 아이템 목록
        elif _return == "Plant":
            $ Craft.slot(PLANT)
        elif _return == "Flower":
            $ Craft.slot(FLOWER)
        elif _return == "Ribbon":
            $ Craft.slot(RIBBON)
        elif _return == "Bug":
            $ Craft.slot(BUG)

        call screen inventory

return