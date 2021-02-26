from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.http import HttpResponse
from accounts.models import Account
from page.models import MyBook, Sentence

# api 사용
import urllib.request
import json

# Create your views here.
# 로그인 여부 확인
def is_login(request):
    if 'user' in request.session:
        return True
    else:
        return False

# 1. 로그인 세션 정보: id
def get_session_id(request):
    id = request.session['user']
    return id

# 2. 로그인 세션 정보: name
def get_session_name(id):
    name = ''
    if Account.objects.filter(acc_id = id).exists():
        name = Account.objects.filter(acc_id = id)[0].acc_name
    return name
    
def home(request):
    if is_login(request):
        id = get_session_id(request)
        name = get_session_name(id)
    else:
        name = None
    return render(request, "home.html", {'name':name})



def mylibrary(request):
    id = get_session_id(request)
    name = get_session_name(id)

    # 기록 가져오기
    if MyBook.objects.filter(acc_id=id).exists(): # 내가 작성한 기록 존재시
        all_books = MyBook.objects.filter(acc_id=id)
        paginator = Paginator(all_books, 6)
        page = request.GET.get('page')
        books = paginator.get_page(page)
        return render(request, "mylibrary.html", {'name':name, 'books':books})
    # 기록 없음
    else:
        return render(request, "mylibrary.html", {'name':name})
    

def detail(request, isbn):
    id = get_session_id(request)
    name = get_session_name(id)
    
    # 책 정보 가져오기
    book_detail = get_object_or_404(MyBook, acc_id = id, isbn=isbn)
    too_long = False
    short_idea = ''
    if book_detail.idea != None and len(book_detail.idea) > 170:
        too_long = True
        short_idea = book_detail.idea[:170]
    
    # 구절 정보 가져오기
    sentences = Sentence.objects.filter(acc_id = id).filter(isbn=isbn)

    return render(request, 'detail.html', {'name':name,'book_detail': book_detail, 'too_long':too_long, 'short_idea': short_idea, 'sentences':sentences})

def add_sentence(request, isbn):
    # 로그인 세션 정보 가져오기
    id = request.session['user']
    name = ''
    if Account.objects.filter(acc_id = id).exists():
        name = Account.objects.filter(acc_id = id)[0].acc_name
    
    # 책 정보 가져오기
    book_detail = get_object_or_404(MyBook, acc_id = id, isbn=isbn)
    # 구절 정보 가져오기
    sentences = Sentence.objects.filter(acc_id = id).filter(isbn=isbn)

    # 구절 추가
    if request.method == 'POST':
        page = request.POST['page']
        sentence = request.POST['sentence']
        # 빈 구절이면 추가하지 않음
        if sentence == '':
            return redirect('/add_sentence/'+str(isbn))
        new_sentence = Sentence(acc_id=id, isbn=isbn, page=page, sentence=sentence)
        new_sentence.save()
        return redirect('/detail/'+str(isbn))

    return render(request, 'add_sentence.html', {'name':name, 'book_detail': book_detail, 'sentences':sentences})

def mod_sentence(request, pk):
    # 로그인 세션 정보 가져오기
    id = request.session['user']
    name = ''
    if Account.objects.filter(acc_id = id).exists():
        name = Account.objects.filter(acc_id = id)[0].acc_name
    
    # 구절 정보 가져오기
    sentence = Sentence.objects.filter(id=pk)[0]
    # 책 정보 가져오기
    book_detail = get_object_or_404(MyBook, acc_id = id, isbn = sentence.isbn)

    # 구절 수정하기
    if request.method=='POST':
        new_page = request.POST['page']
        new_sentence = request.POST['sentence']
        sentence.page = new_page
        sentence.sentence = new_sentence
        sentence.save()
        return redirect('/detail/' + str(sentence.isbn))

    return render(request, 'mod_sentence.html', {'name':name, 'book_detail': book_detail, 'sentence':sentence})


def del_sentence(request, pk):
    # 구절 정보 가져오기
    sentence = Sentence.objects.filter(id=pk)
    isbn = sentence[0].isbn
    sentence.delete()
    return redirect('/detail/' + str(isbn))

def add_idea(request, isbn):
    # 로그인 세션 정보 가져오기
    id = request.session['user']
    name = ''
    if Account.objects.filter(acc_id = id).exists():
        name = Account.objects.filter(acc_id = id)[0].acc_name
    
    # 책 정보 가져오기
    book_detail = get_object_or_404(MyBook, acc_id = id, isbn=isbn)
    
    # 느낀점 수정
    if request.method == 'POST':
        idea = request.POST['idea']
        book_detail.idea = idea
        book_detail.save()
        return redirect('/detail/' + str(isbn))
    
    return render(request, 'add_idea.html', {'name':name,'book_detail': book_detail})

def idea_detail(request, isbn):
    # 로그인 세션 정보 가져오기
    id = request.session['user']
    name = ''
    if Account.objects.filter(acc_id = id).exists():
        name = Account.objects.filter(acc_id = id)[0].acc_name
    
    # 책 정보 가져오기
    book_detail = get_object_or_404(MyBook, acc_id = id, isbn=isbn)

    return render(request, 'idea_detail.html', {'name':name,'book_detail': book_detail})

def add_score(request, isbn):
    id = get_session_id(request)
    name = get_session_name(id)
    
    # 책 정보 가져오기
    book_detail = get_object_or_404(MyBook, acc_id = id, isbn=isbn)
    
    # 점수 수정
    if request.method == 'POST':
        score = request.POST['score']
        book_detail.score = score
        book_detail.save()
        return redirect('/detail/' + str(isbn))
    
    return render(request, 'add_score.html', {'name':name,'book_detail': book_detail})

def add_book(request):
    id = get_session_id(request)
    name = get_session_name(id)
    
    if request.method == 'POST':
        cover = request.POST['cover']
        title = request.POST['title']
        author = request.POST['author']
        publisher = request.POST['publisher']
        pubdate = request.POST['pubdate']
        isbn = request.POST['isbn']
        start = request.POST['start']
        end = request.POST['end']
        if start == '':
            start = None
        if end == '':
            end = None
        
        if multiple_isbn_check(id, isbn):
            return render(request, "add_book.html", {"message":True})

        mybook = MyBook(acc_id = id, image = cover, title=title, author=author, publisher=publisher, pubdate=pubdate, isbn=isbn, start=start, end=end)
        mybook.save()
        return redirect('mylibrary')

    return render(request, "add_book.html", {'name':name})

# 한 아이디 내 중복 isbn 체크
def multiple_isbn_check(id, isbn):
    if MyBook.objects.filter(acc_id=id, isbn=isbn).exists():
        return True
    else:
        return False

# 네이버 도서 검색 api
def book_api(search, type):
    client_id = "X279fyQvsnMBBgGtwaDt" # 애플리케이션 등록시 발급 받은 값 입력
    client_secret = "8aSTAVWHIO" # 애플리케이션 등록시 발급 받은 값 입력
    encText = urllib.parse.quote(search)
    
    url = ""
    if type == "type-all":
        url = "https://openapi.naver.com/v1/search/book?query=" + encText +"&display=10&sort=count"
    elif type == "type-titl":
        url = "https://openapi.naver.com/v1/search/book_adv?d_titl=" + encText +"&display=10&sort=count"
    elif type == "type-auth":
        url = "https://openapi.naver.com/v1/search/book_adv?d_auth=" + encText +"&display=10&sort=count"
    elif type == "type-isbn":
        url = "https://openapi.naver.com/v1/search/book_adv?d_isbn=" + encText +"&display=10&sort=count"
    elif type == "type-publ":
        url = "https://openapi.naver.com/v1/search/book_adv?d_publ=" + encText +"&display=10&sort=count"
    
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        response = response_body.decode('utf-8')
        return response
    else:
        print("Error Code:" + rescode)
        return str(rescode)
    
    return str(rescode)


def search(request):
    if request.method == 'POST':
        type = request.POST['type']
        keyword = request.POST['keyword']

        if keyword == '':
            return redirect('add_book')
        
        response = book_api(keyword, type)
        json_response = json.loads(response) # str -> json 형변환
        results = json_response['items']
        return render(request, "result.html", {'results':results, 'keyword':keyword})

def new_book(request):
    # isbn
    if request.method == 'POST':
        cover = request.POST['cover']
        title = request.POST['title']
        author = request.POST['author']
        publisher = request.POST['publisher']
        pubdate = request.POST['pubdate']
        isbn = request.POST['isbn']
    return render(request, "add_book.html", 
    {'cover':cover, 'title':title, 'author':author, 'publisher':publisher, 'pubdate':pubdate, 'isbn':isbn})

def index(request):
    return render(request, 'index.html')

def generic(request):
    return render(request, 'generic.html')

def elements(request):
    return render(request, 'elements.html')

def tour(request):
    if is_login(request):
        id = get_session_id(request)
        name = get_session_name(id)
    else:
        name = None
    
    all_books = MyBook.objects.all()
    unique_isbn = dict()
    for book in all_books:
        if book.isbn in unique_isbn:
            continue
        else:
            unique_isbn[book.isbn] = book.acc_id
    
    unique_books = []
    for isbn, id in unique_isbn.items():
        book_obj = MyBook.objects.get(acc_id = id, isbn=isbn)
        unique_books.append(book_obj)
    
    paginator = Paginator(unique_books, 9)
    page = request.GET.get('page')
    books = paginator.get_page(page)
    return render(request, "tour.html", {'name':name, 'books':books})

def tour_book(request, isbn):
    if is_login(request):
        id = get_session_id(request)
        name = get_session_name(id)
    else:
        name = None
    
    book = MyBook.objects.filter(isbn=isbn).first()

    comments = []
    score = 0
    total = 0
    for book_objs in MyBook.objects.filter(isbn=isbn):
        name = Account.objects.get(acc_id=book_objs.acc_id).acc_name
        comments.append((name, book_objs.acc_id, book_objs.idea))
        if book_objs.score != None:
            score += int(book_objs.score)
            total += 1
    if total == 0:
        avg_score = 0
    else:
        avg_score = score / total
    
    return render(request, "tour_book.html", {'name':name, 'book':book, 'comments':comments, 'avg_score':avg_score})