class Node(object):
    """데이터와 링크를 가진 노드
    
        item: _item(데이터)의 getter 및 setter.
        next: _next(링크)의 getter 및 setter.
    """
 
    def __init__(self, item):
        self._item = item
        self._next = None
 
    @property
    def item(self):
        return self._item
 
    @item.setter
    def item(self, new_item):
        self._item = new_item
 
    @property
    def next(self):
        return self._next
 
    @next.setter
    def next(self, new_next):
        self._next = new_next


class LinkedList(object):
    """단순 연결 리스트 (Simply Linked List)
 
        is_empty(): 리스트가 비어있다면 True를 반환한다.
        includes(item): item이 리스트에 있다면 True를 반환한다.
        get_size(): 리스트 내 노드의 갯수를 반환한다.
        add(item): item을 리스트 앞에 추가한다.
        append(item): item을 리스트 마지막에 추가한다.
        delete(item): item을 리스트에서 삭제한다. 
        delete_first(): 리스트 첫 노드를 삭제한다. 
        delete_last(): 리스트 마지막 노드를 삭제한다. 
    """
 
    def __init__(self):
        # head: 첫 노드 참조
        self._head = None
 
    def is_empty(self):
        # 연결된 값이 없으면 head가 None이므로 True 반환
        return self._head is None
 
    def includes(self, item):
        current = self._head
 
        while current is not None:
            # 마지막 노드가 아닐 때
            if current.item == item:
                return True
            else:
                # 다음 노드 탐색
                current = current.next
        return False
 
    def get_size(self):
        current = self._head
        count = 0
 
        while current is not None:
            # 마지막 노드에 도달할 때까지
            count += 1
            # current를 다음 노드로 설정
            current = current.next
        return count
 
    def add(self, item):
        new = Node(item)
        # 첫 노드 앞에 new 연결
        new.next = self._head
        # new를 새로운 head로 설정
        self._head = new
 
    def append(self, item):
        new = Node(item)
        if self.is_empty():
            # 첫 노드를 new로 설정
            self._head = new
        else:
            current = self._head
            while current.next is not None:
                current = current.next
            # 마지막에 new 연결
            current.next = new
 
    def delete(self, item):
        current = self._head
        previous = None
 
        # item 탐색
        while True:
            if current.item == item:
                # item 탐색 성공
                break
            else:
                # previous와 current를 뒤로 하나씩 이동
                previous = current
                current = current.next
 
                if current is None:
                    # item이 없을 때
                    raise NotFoundError(item)
 
        if previous is None:
            # 삭제할 item이 첫 노드일 때
            self._head = current.next
        else:
            # item 이전 노드를 item 이후 노드와 연결 (item을 연결 해제)
            previous.next = current.next
 
    def delete_first(self):
        if self.is_empty():
            raise NotFoundError()
        else:
            # head를 두번째 노드에 연결
            self._head = self._head.next
 
    def delete_last(self):
        if self.is_empty():
            raise NotFoundError()
        else:
            current = self._head
            previous = None
            while current.next is not None:
                # current가 마지막에 도달할 때까지
                previous = current
                current = current.next
            # 마지막 노드 연결 해제
            previous.next = None
 
    def print_items(self):
        print(f"{self.__class__.__name__}: ", end="")
        current = self._head
        while current:
            if current.next is not None:
                print(f"{current.item} -> ", end="")
            else:
                print(current.item)
            current = current.next
 
 
class OrderedLinkedList(LinkedList):
    """정렬된 단순 연결 리스트 (오름차순 정렬)"""
 
    def __init__(self):
        super().__init__()
 
    def includes(self, item):
        current = self._head
 
        while current is not None:
            if current.item == item:
                # 발견했을 때
                return True
            else:
                if current.item > item:
                    # 탐색 범위를 넘었을 때
                    break
                else:
                    current = current.next
            return False
 
    def add(self, item):
        current = self._head
        previous = None
 
        while current is not None:
            if current.item > item:
                # 들어갈 위치 발견: previous -> item -> current
                break
            else:
                previous = current
                current = current.next
 
        new = Node(item)
        if previous is None:
            # new가 첫 노드일 때
            new.next = self._head
            self._head = new
        else:
            # previous -> new -> current
            new.next = current
            previous.next = new
 
    def append(self, *args):
        # 정렬된 리스트는 append를 사용할 수 없다.
        raise AttributeError("'OrderedLinkedList' object has no attribute 'append'")
 
 
class NotFoundError(Exception):
    def __init__(self, item=None):
        if item is None:
            detail = "There is no item in the list."
        else:
            detail = f"'{item}' does not exist."
        super().__init__(detail)


class CircularLinkedList(object):
    """환형 연결 리스트 (Circular Linked List)
 
        is_empty(): 리스트가 비어있다면 True를 반환한다.
        includes(item): item이 리스트에 있다면 True를 반환한다.
        add(item): item을 리스트 앞에 추가한다.
        append(item): item을 리스트 마지막에 추가한다.
        delete(item): item을 리스트에서 삭제한다. 
        delete_first(): 리스트 첫 노드를 삭제한다. 
        delete_last(): 리스트 마지막 노드를 삭제한다. 
    """
 
    def __init__(self):
        # head: 마지막 노드 참조
        self._head = None
 
    def is_empty(self):
        return self._head is None
 
    def includes(self, item):
        if self.is_empty():
            raise NotFoundError()
 
        else:
            first_node = self._head.next
            if first_node == first_node.next:
                # 노드가 하나일 때
                if first_node.item == item:
                    return True
                else:
                    return False
            else:
                # 노드가 여러 개일 때
                current = first_node
 
                while True:
                    if current.item == item:
                        return True
                    else:
                        current = current.next
 
                    if current == first_node:
                        # (한 바퀴를 순회했을 때)
                        return False
 
    def add(self, item):
        new = Node(item)
 
        if self.is_empty():
            new.next = new
            self._head = new
        else:
            # new를 첫 노드 앞에 연결
            new.next = self._head.next
            # 마지막 노드를 new에 연결
            self._head.next = new
 
    def append(self, item):
        new = Node(item)
 
        if self.is_empty():
            new.next = new
            self._head = new
        else:
            # new 뒤에 첫 노드 연결
            new.next = self._head.next
            # 마지막 노드를 new와 연결
            self._head.next = new
            # head가 new를 참조
            self._head = new
 
    def delete(self, item):
        last_node = self._head
        previous = last_node
        current = previous.next
 
        while True:
 
            if current.item == item:
                # item을 발견했을 때, 연결 해제
                previous.next = current.next
                break
 
            if current == last_node:
                # item이 없을 때
                raise NotFoundError()
 
            previous = current
            current = current.next
 
    def delete_first(self):
        if self.is_empty():
            raise NotFoundError()
        else:
            first_node = self._head.next
            if first_node == self._head:
                # 리스트 내 값이 하나일 때
                self._head = None
            else:
                # 마지막 노드를 두번쨰 노드에 연결
                self._head.next = first_node.next
 
    def delete_last(self):
        if self.is_empty():
            raise NotFoundError()
        else:
            last_node = self._head
            current = last_node
            while current.next != last_node:
                # current가 마지막 값의 이전 값일 때 반복 종료
                current = current.next
            # current를 첫 노드와 연결
            current.next = last_node.next
            # 마지막 값을 current로 설정
            self._head = current
 
    def print_items(self):
        if self.is_empty():
            print("There is no item in the list.")
 
        current = self._head
        if current == current.next:
            print(f"{current.item} -> (repeat)")
        else:
            first_node = current
            while True:
                current = current.next
                print(current.item, end=" -> ")
                if current == first_node:
                    print("(repeat)")
                    break
 
 
class NotFoundError(Exception):
    def __init__(self):
        super().__init__("There is no item in the list.")


if __name__ == "__main__":
 
    # 연결 리스트 생성 및 노드 생성
    list_ = OrderedLinkedList()
    for i in range(5):
        list_.add(i)
 
    # 연결 리스트 확인
    print()
    print(f"item size: {list_.get_size()}")
    list_.print_items()
 
    # 리스트 값 삭제
    print()
    print("Delete 3")
    list_.delete(3)
    list_.print_items()

    # 환형 리스트 생성 및 노드 생성
    list_ = CircularLinkedList()
    for i in range(5):
        list_.add(i)
 
    # 연결 리스트 확인
    print()
    list_.print_items()
 
    # 리스트 값 삭제
    print()
    print("Delete 2")
    list_.delete(2)
    list_.print_items()