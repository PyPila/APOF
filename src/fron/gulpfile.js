// ///////////////////////////////////////////////////////////////////
// Required
// ///////////////////////////////////////////////////////////////////
var browserSync = require('browser-sync').create(),
    cleanCSS = require('gulp-clean-css'),
    gulp = require('gulp'),
    merge = require('merge-stream'),
    plumber = require('gulp-plumber'),
    rename = require('gulp-rename')
    sass = require('gulp-sass')
    uglify = require('gulp-uglify');


// ///////////////////////////////////////////////////////////////////
// PATHS
// ///////////////////////////////////////////////////////////////////
const statics = {
    portal: {
        static: '../apof/portal/static/portal/',
        templates: '../apof/portal/templates/portal/'
    },
    restaurants: {
        static: '../apof/restaurants/static/restaurants/',
        templates: '../apof/restaurants/templates/restaurants/'
    }
}

const paths = {
    dist: {
        portal: {
            js: statics.portal.static + 'js/',
            css: statics.portal.static + 'css/'
        },
        restaurants: {
            js: statics.restaurants.static + 'js/',
            css: statics.restaurants.static + 'css/'
        }
    },
    deps: {
        portal: {
            js: statics.portal.static + 'js/*.js',
            min_js: statics.portal.static + 'js/*.min.js',
            scss: statics.portal.static + 'scss/*.scss',
            html: statics.portal.templates + '*.html'
        },
        restaurants: {
            js: statics.restaurants.static + 'js/*.js',
            min_js: statics.restaurants.static + 'js/*.min.js',
            scss: statics.restaurants.static + 'scss/*.scss',
            html: statics.restaurants.templates + '*.html'
        }
    }
}


// ///////////////////////////////////////////////////////////////////
// Sass tasks
// ///////////////////////////////////////////////////////////////////
gulp.task('sass', function(){
    var portalPath = gulp.src(paths.deps.portal.scss)
        .pipe(plumber())
        .pipe(sass().on('error', sass.logError))
        .pipe(cleanCSS())
        .pipe(gulp.dest(paths.dist.portal.css))
        .pipe(browserSync.stream()),

        restaurantsPath = gulp.src(paths.deps.restaurants.scss)
        .pipe(plumber())
        .pipe(sass().on('error', sass.logError))
        .pipe(cleanCSS())
        .pipe(gulp.dest(paths.dist.restaurants.css))
        .pipe(browserSync.stream());

    return merge(portalPath, restaurantsPath)
});


// ///////////////////////////////////////////////////////////////////
// JS Tasks
// ///////////////////////////////////////////////////////////////////
gulp.task('scripts', function(){
    var portalPath = gulp.src([paths.deps.portal.js, '!' + paths.deps.portal.min_js])
        .pipe(plumber())
        .pipe(rename({suffix:'.min'}))
        .pipe(uglify())
        .pipe(gulp.dest(paths.dist.portal.js))
        .pipe(browserSync.stream()),

        restaurantsPath = gulp.src([
            paths.deps.restaurants.js,
            '!' + paths.deps.restaurants.min_js
        ])
        .pipe(plumber())
        .pipe(rename({suffix:'.min'}))
        .pipe(uglify())
        .pipe(gulp.dest(paths.dist.restaurants.js))
        .pipe(browserSync.stream());

    return merge(portalPath, restaurantsPath)
});


// ///////////////////////////////////////////////////////////////////
// Browser-Sync Tasks
// ///////////////////////////////////////////////////////////////////
gulp.task('browser-sync', function() {
    browserSync.init({
        proxy: {
            target: 'localhost:8000',
            ws: true
        }
    });
});


// ///////////////////////////////////////////////////////////////////
// HTML Tasks
// ///////////////////////////////////////////////////////////////////
gulp.task('html', function(){
    gulp.src('../**/*.html')
    .pipe(browserSync.stream());
});


// ///////////////////////////////////////////////////////////////////
// Watch tasks
// ///////////////////////////////////////////////////////////////////
gulp.task('sass:watch', function(){
    gulp.watch(
        [paths.deps.portal.scss, paths.deps.restaurants.scss],
        ['sass']
    );
    gulp.watch(
        '../**/*.html',
        ['html']
    );
        gulp.watch(
        [paths.deps.portal.js, paths.deps.restaurants.js],
        ['scripts']
    );
});


// ///////////////////////////////////////////////////////////////////
// Default tasks
// ///////////////////////////////////////////////////////////////////
gulp.task('default', ['sass', 'sass:watch', 'html', 'browser-sync', 'scripts']);
