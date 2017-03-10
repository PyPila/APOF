var browserSync = require('browser-sync').create(),
    gulp = require('gulp'),
    plumber = require('gulp-plumber'),
    sass = require('gulp-sass'),
    uglify = require('gulp-uglify');


const paths = {
    deps: {
        js: [
            'node_modules/bootstrap/dist/js/bootstrap.min.js',
            'bower_components/bootstrap-material-design/dist/bootstrap-material-design-iife.min.js',
            'node_modules/jquery/dist/jquery.min.js',
            'node_modules/tether/dist/js/tether.min.js'
        ],
        css: [
            'node_modules/bootstrap/dist/css/bootstrap.css',
            'bower_components/bootstrap-material-design/dist/bootstrap-material-design.css',
            'node_modules/font-awesome/css/font-awesome.css'
        ],
        fonts: [
            'node_modules/font-awesome/fonts/*.*'
        ]
    }
};


gulp.task('required_deps', function(){
    gulp.src(paths.deps.js)
        .pipe(gulp.dest('dist/js'));
    gulp.src(paths.deps.css)
        .pipe(gulp.dest('dist/css'));
    gulp.src(paths.deps.fonts)
        .pipe(gulp.dest('dist/fonts'));
    gulp.src(paths.deps.js)
        .pipe(gulp.dest('dist/js'));
});


gulp.task('sass', function(){
    return  gulp.src('src/scss/main.scss')
        .pipe(plumber())
        .pipe(sass().on('error', sass.logError))
        .pipe(gulp.dest('dist/css/'))
        .pipe(browserSync.stream());
});


gulp.task('scripts', function(){
    return  gulp.src('src/js/*.js')
        .pipe(plumber())
        .pipe(gulp.dest('dist/js'))
        .pipe(browserSync.stream());
});


gulp.task('images', function(){
    return  gulp.src('src/images/*.*')
        .pipe(plumber())
        .pipe(gulp.dest('dist/images'))
        .pipe(browserSync.stream());
});


gulp.task('browser-sync', function() {
    browserSync.init({
        proxy: {
            target: 'localhost:8000',
            ws: true
        }
    });
});


gulp.task('html', function(){
    gulp.src('../**/*.html')
        .pipe(browserSync.stream());
});


gulp.task('watch', function(){
    gulp.watch(
        ['src/scss/**/*.scss'],
        ['sass']
    );
    gulp.watch(
        '../**/*.html',
        ['html']
    );
    gulp.watch(
        ['src/js/*.js'],
        ['scripts']
    );
    gulp.watch(
        ['src/images/*.*'],
        ['images']
    );
});


gulp.task('build', ['sass','required_deps', 'html', 'scripts', 'images']);


gulp.task('default', ['build', 'watch', 'browser-sync']);
