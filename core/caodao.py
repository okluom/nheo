"""
core/caodao.py — Kho câu ca dao tục ngữ Việt Nam
"""

import random

CAO_DAO = [
    "Công cha như núi Thái Sơn,\nNghĩa mẹ như nước trong nguồn chảy ra.",
    "Bầu ơi thương lấy bí cùng,\nTuy rằng khác giống nhưng chung một giàn.",
    "Nhiễu điều phủ lấy giá gương,\nNgười trong một nước phải thương nhau cùng.",
    "Một cây làm chẳng nên non,\nBa cây chụm lại nên hòn núi cao.",
    "Học ăn, học nói, học gói, học mở.",
    "Đi một ngày đàng, học một sàng khôn.",
    "Uống nước nhớ nguồn.",
    "Có công mài sắt, có ngày nên kim.",
    "Lời nói chẳng mất tiền mua,\nLựa lời mà nói cho vừa lòng nhau.",
    "Gần mực thì đen, gần đèn thì sáng.",
    "Tốt gỗ hơn tốt nước sơn,\nXấu người đẹp nết còn hơn đẹp người.",
    "Ăn quả nhớ kẻ trồng cây.",
    "Chớ thấy sóng cả mà ngã tay chèo.",
    "Gieo gió gặt bão.",
    "Cái khó ló cái khôn.",
    "Thất bại là mẹ thành công.",
    "Đêm tháng năm chưa nằm đã sáng,\nNgày tháng mười chưa cười đã tối.",
    "Mau sao thì nắng, vắng sao thì mưa.",
    "Trăm hay không bằng tay quen.",
    "Làm người phải biết tự lo,\nLo xa lo rộng, lo cho đời mình.",
    "Số giàu đem đến dửng dưng,\nLợi danh đưa tới thì đừng từ nan.",
    "Phúc bất trùng lai, họa vô đơn chí.",
    "Mệnh trời đã định, chớ cầm cầm ngang.",
    "Biết mình biết người trăm trận trăm thắng.",
    "Tiên học lễ, hậu học văn.",
    "Non sông gấm vóc, đất trời bao la.",
    "Trời sinh voi sinh cỏ.",
    "Ở hiền gặp lành.",
    "Khôn ngoan chẳng lọ thật thà,\nDù cho khôn khéo cũng thua người hiền.",
    "Chữ tín còn quý hơn vàng.",
]


def get_random_cao_dao() -> str:
    return random.choice(CAO_DAO)
