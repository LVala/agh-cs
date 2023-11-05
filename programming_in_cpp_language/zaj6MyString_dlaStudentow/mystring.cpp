#include <cstring>
#include <string>
#include <iostream>
#include <algorithm>
#include <iterator>
#include <cstdlib>
#include <vector>
#include <string_view>
#include <iomanip>
#include "mystring.h"

MyString MyString::generateRandomWord(size_t length) {
    MyString new_str;
    for (size_t i=0; i<length; ++i) {
        new_str += 'a' + rand()%26;
    }

    return new_str;
}

MyString::MyString(const char *text) {
    if (strlen(text)<= initialBufferSize) {
        strcpy(text_st, text);
        _size = strlen(text);
        return;
    }

    strncpy(text_st, text, initialBufferSize);
    text_dn = std::string(text+initialBufferSize);
    _size = initialBufferSize + text_dn.size();

}

MyString::MyString(const MyString &text) {
    strncpy(this->text_st, text.text_st, initialBufferSize);
    this->text_dn = text.text_dn;
    _size = text.size();
}

void MyString::clear() {
    text_st[0] = '\0';
    text_dn.clear();
    _size = 0;
}

MyString& MyString::trim() {
    MyString temp(*this);
    this->clear();
    auto it = std::find_if_not(temp.begin(), temp.end(), ::isspace);

    auto end_it = temp.end();
    --end_it;
    while (isspace(*end_it)) --end_it;
    ++end_it;
    while (it != end_it) {
        *this += *it;
        ++it; 
    }

    return *this;
}

std::set<MyString> MyString::getUniqueWords() const {
    std::set<MyString> new_set;
    MyString temp(*this);

    for (size_t i=0; i<_size; ++i) {  // I really cannot be bothered to fight with std::transform
        temp[i] = tolower(temp[i]);
        if (ispunct(temp[i])) temp[i] = ' ';
    }

    size_t cur_index = 0;
    while (cur_index < _size) {
        auto it = std::find_if(iterator(&temp, cur_index), temp.end(), [](int a) {return !isspace(a);});
        auto it_end = std::find_if(it, temp.end(), ::isspace);
        MyString new_str;
        while (it != it_end) {
            new_str += *it;
            ++it;
        }

        if (!new_str.empty()) new_set.insert(new_str);
        cur_index = it_end._index;
    }

    return new_set;
}

std::map<MyString,size_t> MyString::countWordsUsageIgnoringCases() const {
    std::map<MyString, size_t> new_map;
    MyString temp(*this);

    for (size_t i=0; i<_size; ++i) {
        temp[i] = tolower(temp[i]);
        if (ispunct(temp[i])) temp[i] = ' ';
    }

    size_t cur_index = 0;
    while (cur_index < _size) {
        auto it = std::find_if(iterator(&temp, cur_index), temp.end(), [](int a) {return !isspace(a);});
        auto it_end = std::find_if(it, temp.end(), ::isspace);
        MyString new_str;
        while (it != it_end) {
            new_str += *it;
            ++it;
        }

        if (!new_str.empty()) {
            if (new_map.count(new_str))
                new_map[new_str] += 1;
            else
                new_map.insert({new_str, 1});
        }
        cur_index = it_end._index;
    }

    return new_map;


    return new_map;
}

MyString& MyString::toLower() {
    for (size_t i=0; i<_size; ++i) {
        (*this)[i] = std::tolower((*this)[i]);
    }
    return *this;
}

bool MyString::startsWith(const char *text) const {
    std::string str(text);
    auto it = std::search((*this).cbegin(),(*this).cend(), str.begin(), str.end());
    if (it._index == 0) return true;
    return false;
}

bool MyString::endsWith(const char *text) const {
    std::string str(text);
    auto it = std::search(const_iterator(this, 73),(*this).cend(), str.begin(), str.end());
    if (str.size() + it._index == (*this).size()) return true;
    return false;
}

MyString MyString::join(const std::vector<MyString> &texts) const {
    MyString new_str;
    size_t k=0;
    for (MyString text: texts) {
        for (size_t i=0;i<text.size(); ++i) {
            new_str += text[i];
        }
        if (k == texts.size()-1) return new_str;

        for (size_t i=0; i<_size; ++i) {
            new_str += (*this)[i];
        }
        k++;
    }
    return new_str;
}

bool MyString::all_of(std::function<bool(char)> predicate) const {
    for (size_t i=0; i<_size; ++i) {
        if (!predicate((*this)[i])) return false;
    }

    return true;
}

void MyString::push_back(char c) {
    (*this) += c;
}

std::ostream& operator<< (std::ostream& stream, const MyString& text) {
    size_t i=0;
    while (i<text.initialBufferSize && text.text_st[i]) {
        stream << text.text_st[i++];
    }

    if (text.size() > text.initialBufferSize) {
        stream << text.text_dn;
    }
    return stream;
}

std::istream& operator>> (std::istream& stream, MyString& text) {
    char temp = stream.get();
    while (stream.good()) {
        if (text._size < text.initialBufferSize) {
            text.text_st[text._size] = temp;
        }
        else {
            text.text_dn += temp;
        }
        ++text._size;
        temp = stream.get();
    }

    return stream;
}

char& MyString::operator[](size_t index) {
    if (index >= _size) {
        throw std::out_of_range("Index out of range");
    }

    if (index < initialBufferSize) {
        return text_st[index];
    }
    else {
        return text_dn[index-initialBufferSize];
    }
}

char MyString::operator[] (size_t index) const {
    if (index >= _size) {
        throw std::out_of_range("Index out of range");
    }

    if (index < initialBufferSize) {
        return text_st[index];
    }
    else {
        return text_dn[index-initialBufferSize];
    }
}

MyString& MyString::operator+=(char rhc) {
    if (_size < initialBufferSize) {
        text_st[_size] = rhc;
    }
    else {
        text_dn += rhc;
    }
    ++_size;
    return *this;
}

bool MyString::operator==(const MyString& rhs) const {
    if (_size != rhs.size()) return false;

    for (size_t i=0; i<_size; ++i) {
        if ((*this)[i] != rhs[i]) return false;
    }

    return true;
}

bool MyString::operator!=(const MyString& rhs) const {
    return !((*this) == rhs);
}

bool MyString::operator< (const MyString& rhs) const {
    for (size_t i=0; i<this->size() && i<rhs.size(); ++i) {
        if ((*this)[i] < rhs[i]) return true;
        if ((*this)[i] > rhs[i]) return false;
    }

    if (this->size() < rhs.size()) return true;
    return false;
}