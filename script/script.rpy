init python:
    # 아이템 목록
    PLANT = Item('Plant', '식물')
    FLOWER = Item('Flower', '꽃')
    RIBBON = Item('Ribbon', '리본')
    BUG = Item('Bug', '벌레')

    # 조합 레시피
    Craft.recipe(PLANT, FLOWER, RIBBON)
    Craft.recipe(RIBBON, FLOWER, BUG)


## 게임 시작
label start:

    $ inven = Inventory()
    $ Quest.add('quest001', '첫 번째 퀘스트')

    jump quest
    # jump craft

return


label quest:

    call screen quest

return


label craft:

    show screen inventory

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


label quest001:

    "퀘스트 001입니다."
    "꽃과 리본과 식물을 드리겠습니다."

    $ inven.add(FLOWER, 3)
    $ inven.add(RIBBON, 3)
    $ inven.add(PLANT, 3)

    "퀘스트 002도 드리겠습니다."
    $ Quest.add('quest002', '제작을 해보자.')

    "퀘스트 001은 끝났습니다."
    $ Quest.remove('quest001')

    call screen quest

return


label quest002:

    "벌레를 하나 만들어 투입해 봅시다.\n퀘스트 목록으로 나가서 제작 버튼을 누르면 됩니다."

    "퀘스트 002는 끝났습니다."
    $ Quest.remove('quest002')

    "벌레 집어넣는 퀘스트를 드리겠습니다."
    $ Quest.add('quest003', '벌레 투입')

    call screen quest

return


label quest003:

    "쉽지 않네… 아이템 집어넣을 슬롯을 따로 만들어야 하나 제작탭에 포함해야 하나."

return