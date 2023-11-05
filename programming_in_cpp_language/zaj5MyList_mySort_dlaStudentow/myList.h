#ifndef MYLIST_H
#define MYLIST_H

#include <memory>
#include <stdexcept>
#include <iosfwd>

template <typename T>
class MyList {
    public:
        struct Node {
            T value;
            std::unique_ptr<MyList::Node> next = nullptr;
        };
        
        std::unique_ptr<MyList::Node> head;
        int _size;

        typedef T value_type;

        MyList() : head(nullptr), _size(0) {}
        MyList(const MyList&) = delete;
        MyList& operator=(const MyList&) = delete;
        ~MyList() = default;

        int size() const {return _size;};
        void push_front(T value);
        T pop_front();
        T front();
        void insert(T value);
        void remove(T element);

        struct Iterator {
            using difference_type = std::ptrdiff_t;
            using value_type = T;
            using pointer = T*;
            using reference = T&;
            using iterator_category = std::input_iterator_tag;

            Node *previousNode = nullptr;
            Node *currentNode = nullptr;
            friend class MyList;
            
            Iterator() : currentNode(nullptr){};
            Iterator (const std::unique_ptr<MyList::Node>& node) : currentNode(node.get()){};

            Iterator &operator++() {
            if (currentNode != nullptr) {
                previousNode = currentNode;
                currentNode = currentNode->next.get();
                }
            return *this;
            }

            Iterator operator++(int) {
                Iterator tempIter = *this;
                ++*this;
                return tempIter;
            }

            bool operator !=(const Iterator &other) const {
                return this->currentNode != other.currentNode;
            }

            T& operator *() {
                return this->currentNode->value;
            }
        };

        Iterator begin() const {return Iterator(this->head);};
        Iterator end() const {return Iterator(nullptr);};
        Iterator begin() {return Iterator(this->head);};
        Iterator end() {return Iterator(nullptr);};
};

template <typename T>
void MyList<T>::push_front(T value) {
            std::unique_ptr<MyList::Node> newNode = std::make_unique<MyList::Node>();
            newNode->value = value;
            if (head != nullptr) {
                newNode->next = std::move(head);
            }
            head = std::move(newNode);
            ++_size;
        }

template <typename T>
T MyList<T>::pop_front() {
    if (head == nullptr) {
        throw std::out_of_range("List is empty");
    }
    T headValue = head->value;
    head = std::move(head->next);
    --_size;
    return headValue;
}

template <typename T>
T MyList<T>::front() {
    if (head == nullptr) {
        throw std::out_of_range("List is empty");
    }
    return head->value;
}

template <typename T>
void MyList<T>::insert(T new_value) {
    std::unique_ptr<MyList::Node> newNode = std::make_unique<MyList::Node>();
    newNode->value = new_value;


    if (head == nullptr) {
        head = std::move(newNode);
        return;
    }

    Node *cur = head->next.get();
    Node *prev = head.get();

    while (cur != NULL) {
        if (cur->value > new_value && prev->value <= new_value) {
            newNode->next = std::move(prev->next);
            prev->next = std::move(newNode);
            return;
        }

        prev = cur;
        cur = cur->next.get();
    }

    prev->next = std::move(newNode);
}

template <typename T>
void MyList<T>::remove(T element) {
    Node *cur = head.get();
    Node *prev = NULL;
    
    while (cur != NULL) {
        if (cur->value == element) {
            if (prev == NULL) {
                head = std::move(cur->next);
                cur = head.get();
            }
            else if (cur->next == nullptr) {
                prev->next = nullptr;
                cur = NULL;
            }
            else {
                prev->next = std::move(cur->next);
                cur = prev->next.get();
            }
            --_size;
        }
        else {
            prev = cur;
            cur = cur->next.get();
        }
    }
}

template <typename T>
std::ostream& operator<<(std::ostream& os, const MyList<T>& myList) {
    typename MyList<T>::Node * curNode = myList.head.get();

    while(curNode != NULL) {
        os << curNode->value << " ";
        curNode = curNode->next.get();
    }
    return os;
}

#endif